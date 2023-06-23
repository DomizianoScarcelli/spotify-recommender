from pydantic import BaseModel


class Song(BaseModel):
    id: int
    name: str
    artist: str
    album: str
    duration: int
    song_uri: str
    album_uri: str
    song_artist_concat: str
