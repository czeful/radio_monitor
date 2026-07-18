from __future__ import annotations
from models.base import Base
from typing import TYPE_CHECKING
from sqlalchemy import  String, func
from sqlalchemy.orm import Mapped, mapped_column , relationship
from datetime import datetime

if TYPE_CHECKING: 
    from models.song import Song

class Artist(Base):
    __tablename__ = "artists"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default= func.now())
    songs: Mapped[list["Song"]] = relationship(
        "Song",
        secondary="song_artists",
        back_populates="artists",
        lazy="selectin"
    )