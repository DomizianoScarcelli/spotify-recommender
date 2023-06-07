from fastapi import APIRouter
from ..services.SongsService import SongsService
from ..models.Song import Song

router = APIRouter()
service = SongsService()


@router.get("/get-song/", tags=["songs"])
async def get_song(id: int):
    song = service.get_song(id)
    return {"song": song}


@router.post("/create-song/", tags=["songs"])
async def create_song(data: Song):
    song = service.create_song(data)
    return {"message": "Song created!", "song": song}
