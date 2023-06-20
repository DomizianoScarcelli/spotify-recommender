from pydantic import BaseModel


class SongRequest(BaseModel):
    song_uri: str
    album_uri: str
