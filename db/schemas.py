from typing import List, Optional
from pydantic import BaseModel, validator
import base64

class TrackBase(BaseModel):
    title: str
    content_type: str

class TrackCreate(TrackBase):
    data: bytes

class Track(TrackBase):
    id: int

    class Config:
        orm_mode = True

class AlbumBase(BaseModel):
    name: str

class AlbumCreate(AlbumBase):
    artist_id: int
    photo: Optional[bytes] = None
    tracks: Optional[List[TrackCreate]] = []

class Album(AlbumBase):
    id: int
    photo: Optional[str] = None
    tracks: List[Track] = []

    class Config:
        orm_mode = True

    @validator('photo', pre=True, always=True)
    def encode_photo(cls, v):
        if v is None:
            return None
        return base64.b64encode(v).decode('utf-8')

class ArtistBase(BaseModel):
    name: str

class ArtistCreate(ArtistBase):
    photo: Optional[bytes] = None

class Artist(ArtistBase):
    id: int
    photo: Optional[str] = None
    albums: List[Album] = []

    class Config:
        orm_mode = True

    @validator('photo', pre=True, always=True)
    def encode_photo(cls, v):
        if v is None:
            return None
        return base64.b64encode(v).decode('utf-8')
