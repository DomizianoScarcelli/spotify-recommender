from fastapi import APIRouter
from ..services.SongsService import SongsService
from ..models.Song import Song
from typing import List

router = APIRouter()
service = SongsService()


@router.get("/")
async def home():
    return {"Message": "Welcome to the song service!"}


@router.get("/get-song", tags=["songs"])
async def get_song(id: int):
    song = service.get_song(id)
    return {"song": song}


@router.post("/create-song", tags=["songs"])
async def create_song(data: Song):
    song = service.create_song(data)
    return {"message": "Song created!", "song": song}


@router.post("/create-songs-batch", tags=["songs"])
async def create_song(data: List[Song]):
    service.create_batch_songs(data)
    return {"message": f"Created {len(data)} songs!"}


@router.get("/search-song", tags=["songs"])
async def search_song(query: str):
    song = service.search_song(query)
    return song


@router.get("/all-songs", tags=["songs"])
async def get_all_songs(page: int = 1):
    song = service.get_all_songs(page)
    return song


@router.delete("/drop-database", tags=["songs"])
async def drop_database():
    song = service.drop_database()
    return song


@router.post("/continuate-playlist", tags=["playlist"])
async def continuate_playlist(songs: List[Song]):
    pass
