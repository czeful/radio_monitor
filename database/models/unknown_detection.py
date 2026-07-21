from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from database.enums import ProcessingStatus

if TYPE_CHECKING:
    from models.song import Song
    from models.audio_segment import AudioSegment


class UnknownDetection(Base):
    __tablename__ = "unknown_detections"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column()
    audio_segment_id: Mapped[int] = mapped_column(ForeignKey("audio_segment.id"), nullable=False)
    song_id: Mapped[int | None] = mapped_column(ForeignKey("songs.id"), nullable=True)
    fingerprint: Mapped[str] = mapped_column(String(64))
    audio_fragment_path: Mapped[str] = mapped_column(String(512), nullable=False)
    classification_result: Mapped[dict] = mapped_column(JSON, nullable=False) 
    status: Mapped[ProcessingStatus] = mapped_column(default=ProcessingStatus.PENDING, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    song: Mapped[Song | None] = relationship("Song", back_populates="unknown_detections", lazy="selectin")
    audio_segment: Mapped[AudioSegment] = relationship("AudioSegment", back_populates="unknown_detections", lazy="selectin")