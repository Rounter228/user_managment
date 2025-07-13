from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    photo = Column(LargeBinary, nullable=True)

    albums = relationship("Album", back_populates="artist", cascade="all, delete-orphan")

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    photo = Column(LargeBinary, nullable=True)

    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album", cascade="all, delete-orphan")

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"))
    content_type = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)

    album = relationship("Album", back_populates="tracks")
