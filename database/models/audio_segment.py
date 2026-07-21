from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
 
from sqlalchemy import DateTime, func, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.unknown_detection import UnknownDetection
    from models.radio_file import RadioFile

class AudioSegment(Base):
    __tablename__ = "audio_segment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    radio_file_id: Mapped[int] = mapped_column(ForeignKey("radio_file.id"))
    file_path:     Mapped[str] = mapped_column(String(255), nullable=False)
    start_time:    Mapped[datetime] = mapped_column(nullable=False)
    end_time:      Mapped[datetime] = mapped_column(nullable=False)
    created_at:    Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at:    Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    unknown_detections: Mapped[list[UnknownDetection]] = relationship("UnknownDetection", back_populates="audio_segment", lazy="selectin")
    radio_file: Mapped["RadioFile"] = relationship("RadioFile", back_populates="audio_segment", lazy="selectin" )