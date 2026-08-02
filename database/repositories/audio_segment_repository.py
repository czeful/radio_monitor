from __future__ import annotations
from database.repositories.base_repository import BaseRepository
from typing import TYPE_CHECKING
from datetime import datetime


from database.models.radio_file import RadioFile 
from database.enums import ProcessingStatus
from database.models.audio_segment import AudioSegment
from sqlalchemy import select, delete 

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

class AudioSegmentRepository(BaseRepository[AudioSegment]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=AudioSegment)
    
    async def delete_old_segments(self, radio_file_id: int) -> int:
        
        """
            Deletes all segments for radio_file_id ONLY if the file itself
            has a ProcessingStatus.COMPLETED status.
            Returns the number of segments deleted. 
        """
        file_status_query = select(RadioFile.id).where(RadioFile.status == ProcessingStatus.COMPLETED, RadioFile.id == radio_file_id).scalar_subquery()

        query = delete(AudioSegment).where(AudioSegment.radio_file_id == file_status_query)
        result = await self.session.execute(query)
        return result.rowcount


    async def get_by_radio_file_id(self, radio_file_id:int) -> list[AudioSegment]:
        query = select(AudioSegment).where(AudioSegment.radio_file_id == radio_file_id).order_by(AudioSegment.radio_file_id)
        result = await self.session.execute(query)

        return list(result.scalars().all())