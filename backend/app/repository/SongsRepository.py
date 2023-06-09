from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import os
from ..models.Song import Song
from ..utils.json_utils import parse_json
from ..utils.aggregator_functions import levenshtein_distance
from bson.code import Code


class SongRepository:
    def __init__(self):
        self.client = MongoClient(
            os.environ["DATABASE_URL"], username="admin", password="password")
        self.db: Database[Song] = self.client['songs_db']
        self.collection: Collection[Song] = self.db["songs"]

    def create_song(self, data: Song):
        song = data.dict()
        self.collection.insert_one(song)
        print(song)
        return parse_json(song)

    def get_song(self, id):
        song = self.collection.find_one({'id': id})
        return parse_json(song)

    def search_song(self, query):
        # Calculate Levenshtein distance in MongoDB using aggregation
        pipeline = [
            {
                "$addFields": {
                    "levenshteinDistance": {
                        "$let": {
                            "vars": {
                                "query": query
                            },
                            "in": {
                                "$function": {
                                    "body": levenshtein_distance,
                                    "args": ["$$query", "$name"],
                                    "lang": "js"
                                }
                            }
                        }
                    }
                }
            },
            {
                "$sort": {"levenshteinDistance": 1}
            }
        ]

        # Execute aggregation pipeline
        result = self.collection.aggregate(pipeline)

        # Convert the results to a list of dictionaries
        songs = [parse_json(song) for song in result]

        return songs
