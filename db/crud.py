from sqlalchemy.orm import Session
from . import models, schemas

def create_artist(db: Session, artist: schemas.ArtistCreate):
    db_artist = models.Artist(name=artist.name, photo=artist.photo)
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

def get_artist(db: Session, artist_id: int):
    return db.query(models.Artist).filter(models.Artist.id == artist_id).first()

def create_album(db: Session, album: schemas.AlbumCreate):
    db_album = models.Album(name=album.name, artist_id=album.artist_id, photo=album.photo)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)

    for track in album.tracks:
        db_track = models.Track(
            title=track.title,
            content_type=track.content_type,
            data=track.data,
            album_id=db_album.id
        )
        db.add(db_track)
    db.commit()
    return db_album

def get_album(db: Session, album_id: int):
    return db.query(models.Album).filter(models.Album.id == album_id).first()

def create_track(db: Session, track: schemas.TrackCreate, album_id: int):
    db_track = models.Track(
        title=track.title,
        content_type=track.content_type,
        data=track.data,
        album_id=album_id
    )
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track

def get_track(db: Session, track_id: int):
    return db.query(models.Track).filter(models.Track.id == track_id).first()

def delete_artist(db: Session, artist_id: int):
    artist = get_artist(db, artist_id)
    if artist:
        db.delete(artist)
        db.commit()
    return artist

def delete_album(db: Session, album_id: int):
    album = get_album(db, album_id)
    if album:
        db.delete(album)
        db.commit()
    return album

def delete_track(db: Session, track_id: int):
    track = get_track(db, track_id)
    if track:
        db.delete(track)
        db.commit()
    return track
