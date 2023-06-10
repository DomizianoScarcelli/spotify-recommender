from ..repository.SongsRepository import SongRepository


class SongsService:
    def __init__(self):
        self.repository = SongRepository()

    def create_song(self, data):
        return self.repository.create_song(data)

    def create_batch_songs(self, data):
        for song in data:
            self.repository.create_song(song)

    def get_song(self, id):
        return self.repository.get_song(id)

    def search_song(self, query: str):
        return self.repository.search_song(query)

    def get_all_songs(self, page: int = 1):
        return self.repository.get_all_songs(page)

    def drop_database(self):
        return self.repository.drop_database()
