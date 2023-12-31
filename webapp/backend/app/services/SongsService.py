from repository.SongsRepository import SongRepository
from models.Responses import PaginatedSongs
from typing import List
from models.Requests import SongRequest
from services.recommendations.UserBasedRecommender import UserBasedRecommender
import base64


class SongsService:
    def __init__(self):
        self.repository = SongRepository()
        self.user_based_recommender = UserBasedRecommender()

    def create_song(self, data):
        return self.repository.create_song(data)

    def create_batch_songs(self, data):
        for song in data:
            self.repository.create_song(song)

    def get_song(self, id):
        return self.repository.get_song(id)

    def get_song_by_uri(self, uri: str):
        return self.repository.get_song_by_uri(uri)

    def get_songs_by_album(self, album_uri: str):
        return self.repository.get_songs_by_album(album_uri)

    def search_song(self, query: str):
        return self.repository.search_song(query)

    def get_all_songs(self, page: int = 1) -> PaginatedSongs:
        songs = self.repository.get_all_songs(page)
        return {"songs": songs, "next_page": page+1}

    def get_album_art(self, album_uri: str) -> bytes:
        image = self.repository.get_album_art(album_uri)
        return image

    def drop_database(self):
        return self.repository.drop_database()

    def continuate_playlist(self, songs: List[SongRequest]):
        return self.user_based_recommender.perform_recommendation(songs)
