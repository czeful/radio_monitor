from __future__ import annotations
from repositories.base_repository import BaseRepository
from typing import TYPE_CHECKING 
from models.detection import Detection
from datetime import datetime
from sqlalchemy import select, delete, update, func, exists
from database.enums import DetectionStatus , MatchType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class DetectionRepository(BaseRepository[Detection]): 
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Detection )
    

    '''
        get_history - вывод N количество детекшнов, не зависимо от песни
    '''
    async  def get_history(self, limit:int) -> list[Detection] :
        query = select(Detection).order_by(Detection.created_at.desc()).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())


    '''
        get_by_song - Данный метод показывает все обьекты таблицы detection по song_id. Грубо говоря всю истории детекшна 
        исменно одной песни. Тут суть в том что пока Detection.status не будет равен Matched он может меняться
        или если confidence низкий
    '''
    async  def get_by_song(self, song_id: int ) -> list[Detection] | None:
        query = select(Detection).where(Detection.song_id == song_id).order_by(Detection.created_at)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_by_date(
        self,
        start_date: datetime,
        end_date: datetime,
        song_id: int | None = None,  
        limit: int = 100,
        offset: int = 0 
        ) -> list[Detection]:
   
        query = (
            select(Detection)
            .where(Detection.created_at >= start_date)
            .where(Detection.created_at < end_date)
        )
    
        #  Если передан song_id, сужаем поиск до конкретной песни
        if song_id is not None:
            query = query.where(Detection.song_id == song_id)
        
        query = (
            query.order_by(Detection.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
    
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def count_detections(
            self,
            song_id: int | None = None,
            match_type: MatchType | None = None,
            status: DetectionStatus | None = None
            ) -> int | None:
        
        query = select(func.count(Detection.id))

        #  Если передан song_id, сужаем поиск до конкретной песни        
        if song_id is not None:
            query = query.where(Detection.song_id == song_id)
        #  Если передан match_type, сужаем поиск до конкретного типа (Fingerprint, ML models, или руками)
        if match_type is not None:
            query = query.where(Detection.match_type == match_type)
        #  Если передан status, сужаем поиск до конкретного статуса (нашелся, не нашеклся, ошибка)
        if status is not None:
            query = query.where(Detection.status == status)

        count_result = await self.session.scalar(query)
        return count_result or 0
        