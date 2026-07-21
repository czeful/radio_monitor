from __future__ import annotations
from repositories.base_repository import BaseRepository
from typing import TYPE_CHECKING 
from models.song import Song
from sqlalchemy import select, delete, update, func, exists
from database.enums import MusicClass

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SongRepository(BaseRepository[Song]): 
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Song)
    
    async def get_by_title(self, song_title: str) -> list[Song] | None:
        query = select(Song).where(Song.title == song_title).order_by(Song.id)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_by_class(self, music_class: MusicClass) -> list[Song] | None:
        query = select(Song).where(Song.music_class == music_class).order_by(Song.id)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def exists_by_title(self, song_title: str) -> bool:
        query =  select(exists().where(Song.title == song_title))
        result = await self.session.execute(query)
        return bool(result.scalar)