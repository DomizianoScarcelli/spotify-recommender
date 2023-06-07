from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import os
from ..models.Song import Song


class SongRepository:
    def __init__(self):
        self.client = MongoClient(os.environ["DATABASE_URL"])
        self.db: Database[Song] = self.client['songs_db']
        self.collection: Collection[Song] = self.collection["songs"]

    def create_song(self, data):
        song = Song(**data).dict()
        self.collection.insert_one(song)

    def get_song(self, id):
        return self.collection.find_one({'id': id})
