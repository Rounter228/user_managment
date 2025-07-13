from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from fastapi import status
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from db import crud, schemas
from db.database import Base, engine, get_db
import io

app = FastAPI(title="Audio Server")

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/artists/", response_model=schemas.Artist)
async def create_artist(
    name: str = Form(...),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    photo_bytes = await photo.read() if photo else None
    artist_in = schemas.ArtistCreate(name=name, photo=photo_bytes)
    return crud.create_artist(db, artist_in)


@app.get("/artists/{artist_id}", response_model=schemas.Artist)
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = crud.get_artist(db, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Виконавець не знайден")
    return artist



@app.post("/albums/", response_model=schemas.Album)
async def create_album(
    name: str = Form(...),
    artist_id: int = Form(...),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    photo_bytes = await photo.read() if photo else None
    album_in = schemas.AlbumCreate(name=name, artist_id=artist_id, photo=photo_bytes, tracks=[])
    return crud.create_album(db, album_in)


@app.get("/albums/{album_id}", response_model=schemas.Album)
def get_album(album_id: int, db: Session = Depends(get_db)):
    album = crud.get_album(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Альбом не знайдено")
    return album



@app.post("/albums/{album_id}/tracks/", response_model=schemas.Track)
async def upload_track(
    album_id: int,
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    file_data = await file.read()
    track_in = schemas.TrackCreate(title=title, content_type=file.content_type, data=file_data)
    album = crud.get_album(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Альбом не знайдено")
    return crud.create_track(db, track_in, album_id)


@app.get("/tracks/{track_id}", response_class=StreamingResponse)
def stream_track(track_id: int, db: Session = Depends(get_db)):
    track = crud.get_track(db, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Пісню не знайдено")
    return StreamingResponse(io.BytesIO(track.data), media_type=track.content_type)


@app.get("/tracks/info/{track_id}", response_model=schemas.Track)
def get_track_info(track_id: int, db: Session = Depends(get_db)):
    track = crud.get_track(db, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Пісню не знайдено")
    return track


@app.delete("/artists/{artist_id}", response_model=schemas.Artist, status_code=status.HTTP_200_OK)
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = crud.delete_artist(db, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Виконавець не знайден")
    return artist

@app.delete("/albums/{album_id}", response_model=schemas.Album, status_code=status.HTTP_200_OK)
def delete_album(album_id: int, db: Session = Depends(get_db)):
    album = crud.delete_album(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Альбом не знайден")
    return album

@app.delete("/tracks/{track_id}", response_model=schemas.Track, status_code=status.HTTP_200_OK)
def delete_track(track_id: int, db: Session = Depends(get_db)):
    track = crud.delete_track(db, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Пісню не знайдено")
    return track
