from repository.SongsRepository import SongRepository
from models.Responses import PaginatedSongs
from typing import List
from models.Requests import SongRequest
from services.recommendations.BaseRecommender import BaseRecommender


class SongsService:
    def __init__(self):
        self.repository = SongRepository()
        self.base_recommender = BaseRecommender()

    def create_song(self, data):
        return self.repository.create_song(data)

    def create_batch_songs(self, data):
        for song in data:
            self.repository.create_song(song)

    def get_song(self, id):
        return self.repository.get_song(id)

    def search_song(self, query: str):
        return self.repository.search_song(query)

    def get_all_songs(self, page: int = 1) -> PaginatedSongs:
        songs = self.repository.get_all_songs(page)
        return {"songs": songs, "next_page": page+1}

    def get_album_art(self, album_uri: str) -> str:
        return self.repository.get_album_art(album_uri)

    def drop_database(self):
        return self.repository.drop_database()

    def continuate_playlist(self, songs: List[SongRequest]):
        return songs
