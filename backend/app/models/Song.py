from pydantic import BaseModel


class Song(BaseModel):
    id: int
    name: str
    artist: str
    album: str
    duration: int
