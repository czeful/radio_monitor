from __future__ import annotations

from database.models.base import Base
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, func, String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database.enums import ProcessingStatus


if TYPE_CHECKING:
    from models.audio_segment import AudioSegment


class RadioFile(Base): 
    __tablename__ = "radio_file"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    filepath: Mapped[str] = mapped_column(String(255), nullable=False)
    duration: Mapped[int | None] = mapped_column() 
    status: Mapped[ProcessingStatus] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    audio_segments: Mapped[list["AudioSegment"]] = relationship("AudioSegment", back_populates="radio_file", lazy = "selectin")

