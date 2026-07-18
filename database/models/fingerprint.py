from models.base import Base
from sqlalchemy import String, ForeignKey, func
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column , relationship
from datetime import datetime

if TYPE_CHECKING:
    from models.song import Song

class Fingerprint(Base):
    __tablename__ = "fingerprints"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    song_id: Mapped[int] = mapped_column(ForeignKey["songs.id"])
    hash: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(server_default= func.now())
    
    song: Mapped["Song"] = relationship("Song" , back_populates="fingerprints", lazy="selectin")