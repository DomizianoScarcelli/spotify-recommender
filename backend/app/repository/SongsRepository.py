from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import os
from ..models.Song import Song
from ..utils.json_utils import parse_json


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
