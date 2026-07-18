from __future__ import annotations
from models.base import Base
from typing import TYPE_CHECKING
from sqlalchemy import  ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from datetime import datetime
from database.enums import MatchType, DetectionStatus


if TYPE_CHECKING:
    from models.song import Song

class Detection(Base):
    __tablename__ = "detections"
    id: Mapped[int | None] = mapped_column(primary_key=True, autoincrement=True)
    song_id: Mapped[int | None] = mapped_column(ForeignKey("songs.id"))
    match_type: Mapped[MatchType] = mapped_column(nullable=False)
    status: Mapped[DetectionStatus]= mapped_column(nullable=False)
    confidence : Mapped[float] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default= func.now())    

    song: Mapped["Song"] = relationship("Song" , back_populates="detections", lazy="selectin")