from __future__ import annotations
from repositories.base_repository import BaseRepository
from typing import TYPE_CHECKING 
from datetime import datetime
from models.unknown_detection import UnknownDetection
from sqlalchemy import select, delete, update, func, exists
from database.enums import ProcessingStatus
if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UnknownDetectionRepository(BaseRepository[UnknownDetection]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=UnknownDetection)

    
    async def get_pending(
            self,
            limit: int,
            offset:int = 0
            ) -> list[UnknownDetection]:
        
        query = select(UnknownDetection).where(UnknownDetection.status == "PENDING")  
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def mark_processed(self, unknown_detection_id: int, status: ProcessingStatus) -> UnknownDetection:
        
        query = (
            update(self.model)
            .where(UnknownDetection.id == unknown_detection_id)
            .values(status = status)
        )
        await self.session.execute(query)
        await self.session.flush()
        
        return await self.get_by_id(unknown_detection_id)
    
    async def get_by_date(
        self,
        start_date: datetime,
        end_date: datetime,
  
        limit: int = 100,
        offset: int = 0 
        ) -> list[UnknownDetection]:    
   
        query = (
            select(UnknownDetection)
            .where(UnknownDetection.created_at >= start_date)
            .where(UnknownDetection.created_at < end_date)
        )

        query = (
            query.order_by(UnknownDetection.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
    
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
