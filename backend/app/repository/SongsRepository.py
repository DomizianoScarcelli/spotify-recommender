from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import os
from ..models.Song import Song
from ..utils.json_utils import parse_json
from ..utils.aggregator_functions import levenshtein_distance, string_char_distance

from typing import List


class SongRepository:
    def __init__(self):
        self.client = MongoClient(
            os.environ["DATABASE_URL"], username="admin", password="password")
        self.db: Database[Song] = self.client['songs_db']
        self.collection: Collection[Song] = self.db["songs"]
        self.search_song_cursor_id = None

    def create_song(self, data: Song):
        song = data.dict()
        enhanced_song = {
            **song, "song_artist_concat": f'{song["name"]} {song["artist"]}'}
        self.collection.insert_one(enhanced_song)
        print(enhanced_song)
        return parse_json(enhanced_song)

    def get_song(self, id):
        song = self.collection.find_one({'id': id})
        return parse_json(song)

    def search_song(self, query):
        # TODO: put an id here
        if self.search_song_cursor_id is not None:
            self.collection.kill_cursors([self.search_song_cursor_id])
        query_spec = {"song_artist_concat": {
            "$regex": f".*{query}.*", "$options": "i"}}

        try:
            songs = self.collection.find(query_spec).limit(10)
            self.search_song_cursor_id = songs.cursor_id
        except IndexError as e:
            return []
        result = []

        for song in songs:
            clean_song = {
                "id": song["id"],
                "name": song["name"],
                "artist": song["artist"],
                "album": song["album"],
                "duration": song["duration"],
                "similarity": {
                    "matchCount": len(query),
                    "matchingPositions": []  # TODO: implement this
                },
            }
            result.append(clean_song)
        return result

        return
        # Calculate Levenshtein distance in MongoDB using aggregation
        pipeline = [
            {
                "$addFields": {
                    "similarity": {
                        "$let": {
                            "vars": {
                                "query": query
                            },
                            "in": {
                                "$function": {
                                    "body": string_char_distance,
                                    "args": ["$$query", "$name"],
                                    "lang": "js"
                                }
                            }
                        }
                    }
                }
            },
            {
                "$sort": {"similarity": -1}
            }
        ]

        # Execute aggregation pipeline
        result = self.collection.aggregate(pipeline)

        LIMIT = 10
        # Convert the results to a list of dictionaries
        songs = [parse_json(song)
                 for index, song in enumerate(result) if index <= LIMIT]

        return songs

    def get_all_songs(self, page: int = 1) -> List[Song]:
        PAGE_SIZE = 50
        skip = (page-1) * PAGE_SIZE
        songs = self.collection.find().skip(skip).limit(PAGE_SIZE)
        return parse_json(songs)

    def drop_database(self):
        self.collection.delete_many({})
