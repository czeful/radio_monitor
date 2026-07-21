from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import select, delete, update, exists, func
from models.artist import Artist
from repositories.base_repository import BaseRepository
if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

class ArtistRepository(BaseRepository[Artist]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Artist)
    
    """
    Мысли:
         Метод  get_by_name -  это поиск артистов по имени, однако насколько часто бывет такео
         что у разных артистов могут быть одинаковые имена?, что бы избежать ошибок решил возвразать ответ
         в виде списка. Возможно имеет смысл возвращаь не список обьектов а просто обьект? Чуть позже нужно решить

         get_by_name method  - searches for artists by name, but since it's so common for different artists
         to have the same name, I decided to return the response as a list to avoid errors. Perhaps it makes more
         sense to return just an object instead of a list of objects? I'll have to decide that later.
    """
    async def get_by_name(self, artist_name:str) -> list[Artist]| None:
        query = select(Artist).where(Artist.name == artist_name).order_by(Artist.id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def exists_by_name(self, artist_name: str) -> bool:
        query =  select(exists().where(Artist.name == artist_name))
        result = await self.session.execute(query)
        return bool(result.scalar)    