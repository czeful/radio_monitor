from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar, Generic

from sqlalchemy import select, delete, update

from models.base import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

# Указываем, что T — это подкласс нашей Base
T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):

    # Используем type[T], чтобы передавать сам класс (например, Song), а не его объект
    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, object_id: int) -> T | None:
        query = select(self.model).where(self.model.id == object_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_ids(self, list_ids: list[int]) -> list[T]:
        if not list_ids:
            return []
        query = select(self.model).where(self.model.id.in_(list_ids))
        result = await self.session.execute(query)
        return list(result.scalars().all())   

    async def get_all(self, limit: int = 20, offset: int = 0) -> list[T]:
        query = select(self.model).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create_object(self, **kwargs) -> T:
        new_object = self.model(**kwargs)
        self.session.add(new_object)
        await self.session.flush()
        return new_object

    async def delete_object(self, base: T) -> None:
        await self.session.delete(base)

    async def delete_object_by_id(self, object_id: int) -> None:
        query = delete(self.model).where(self.model.id == object_id)
        await self.session.execute(query)
    
    async def update_object(self, object_id: int, **kwargs) -> T | None:

        if not kwargs:
            return await self.get_by_id(object_id)

        query = (
            update(self.model)
            .where(self.model.id == object_id)
            .values(**kwargs)
        )
        await self.session.execute(query)
        await self.session.flush()
        
        return await self.get_by_id(object_id)