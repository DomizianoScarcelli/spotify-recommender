from typing import List
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import os
from models.Song import Song
from utils.json_utils import parse_json
from clients.MinioClient import MinioClient


class SongRepository:
    def __init__(self):
        self.client = MongoClient(
            os.environ["DATABASE_URL"], username="admin", password="password")
        self.minio_client = MinioClient()
        self.db: Database[Song] = self.client['songs_db']
        self.collection: Collection[Song] = self.db["songs"]

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

    def get_song_by_uri(self, uri: str):
        song = self.collection.find_one({'song_uri': uri}, {'_id': 0})
        return song

    def get_songs_by_album(self, album_uri: str) -> List[Song]:
        songs = list(self.collection.find(
            {'album_uri': album_uri}, {'_id': 0}))
        return songs

    def search_song(self, query):
        query_spec = {"song_artist_concat": {
            "$regex": f".*{query}.*", "$options": "i"}}

        try:
            songs = self.collection.find(query_spec).limit(10)
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
                "song_uri": song["song_uri"],
                "album_uri": song["album_uri"],
                "song_artist_concat": song["song_artist_concat"],
                "similarity": {
                    "matchCount": len(query),
                    "matchingPositions": []  # TODO: implement this
                },
            }
            result.append(clean_song)
        return result

    def get_all_songs(self, paginated: bool = True, page: int = 1) -> List[Song]:
        print("getting songs")
        if paginated:
            PAGE_SIZE = 50
            skip = (page-1) * PAGE_SIZE
            songs = self.collection.find().skip(skip).limit(PAGE_SIZE)
        else:
            songs = self.collection.find()
        return parse_json(songs)

    def get_album_art(self, album_uri: str) -> bytes:
        image = self.minio_client.get_object(album_uri)
        return image

    def drop_database(self):
        self.collection.delete_many({})
