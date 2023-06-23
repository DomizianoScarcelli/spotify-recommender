from pydantic import BaseModel
from .Song import Song
from typing import List


class PaginatedSongs(BaseModel):
    songs: List[Song]
    next_page: int
