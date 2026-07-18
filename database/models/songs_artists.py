from models.base import Base
from sqlalchemy import Column, Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class SongArtist(Base):
    __tablename__ = "song_artists"
    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id") , primary_key=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), nullable=True, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default= func.now())