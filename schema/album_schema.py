from pydantic import BaseModel
from typing import Optional

class AlbumSchema(BaseModel):
    id: int | None = None 
    name_album: str
    url_spotify: str
    image: str
    release_date: str