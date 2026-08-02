from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base
from database.enums import MusicClass
from database.models.songs_artists import SongArtist

if TYPE_CHECKING:
    from database.models.artist import Artist
    from database.models.detection import Detection
    from database.models.fingerprint import FingerPrint
    from database.models.unknown_detection import UnknownDetection

    
class Song(Base):
    __tablename__ = "songs"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str | None] = mapped_column(String(255))
    duration: Mapped[int | None] = mapped_column()
    music_class: Mapped[MusicClass | None] = mapped_column()
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    artists: Mapped[list[Artist]] = relationship("Artist", secondary="song_artists", back_populates="songs", lazy="selectin")
    detections: Mapped[list[Detection]] = relationship("Detection", back_populates="song")
    fingerprints: Mapped[list[FingerPrint]] = relationship("FingerPrint", back_populates="song")
    unknown_detections: Mapped[list[UnknownDetection]] = relationship("UnknownDetection", back_populates="song")