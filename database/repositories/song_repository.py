from __future__ import annotations
from database.repositories.base_repository import BaseRepository
from typing import TYPE_CHECKING 
from database.models.song import Song
from sqlalchemy import select, exists, func
from database.models.songs_artists import SongArtist
from database.enums import MusicClass

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SongRepository(BaseRepository[Song]): 
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Song)
    
    async def get_by_title(
            self,
            song_title: str,
            limit: int = 10,
            offset: int = 0
            ) -> list[Song]:
        
        query = (
            select(Song).
            where(Song.title == song_title)
            .order_by(Song.id)
            .limit(limit=limit)
            .offset(offset=offset)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_by_class(
            self,
            music_class: MusicClass, 
            limit: int = 10,
            offset: int = 0
            ) -> list[Song]:
        query = (
            select(Song)
            .where(Song.music_class == music_class)
            .order_by(Song.id)
            .limit(limit=limit)
            .offset(offset=offset)
            )
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def exists_by_title(self, song_title: str) -> bool:
        query =  select(exists().where(Song.title == song_title))
        result = await self.session.execute(query)
        return bool(result.scalar())


    #TODO Написать под него тесы, это новый метод
    async def exists_by_title_and_artists(
            self, 
            title: str, 
            artist_ids: list[int]
    ) -> bool:
        """
        Proves whether a song with the same title and the exact same set of artists (by ID) already exists.
        """
        if not artist_ids:
            return False

        artist_ids = sorted(set(artist_ids))
        expected_count = len(artist_ids)

        stmt = (
            select(Song.id)
            .join(SongArtist, Song.id == SongArtist.song_id)
            .where(
                Song.title == title,
                SongArtist.artist_id.in_(artist_ids),
            )
            .group_by(Song.id)
            .having(func.count(SongArtist.artist_id) == expected_count)
            .limit(1)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

