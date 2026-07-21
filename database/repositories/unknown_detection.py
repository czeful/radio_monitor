from __future__ import annotations
from repositories.base_repository import BaseRepository
from typing import TYPE_CHECKING 
from models.unknown_detection import UnknownDetection
from sqlalchemy import select, delete, update, func, exists

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UnknownDetectionRepository(BaseRepository[UnknownDetection]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=UnknownDetection)

    
    async def get_pending(
            self,
            limit: int,
            offset: 0
            ) -> list[UnknownDetection]:
        
        query = ()