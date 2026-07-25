from __future__ import annotations
from typing import TYPE_CHECKING


from sqlalchemy import  update
from models.radio_file import RadioFile
from repositories.base_repository import BaseRepository
from database.enums import ProcessingStatus
if  TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession 



class RadioFileRepository(BaseRepository[RadioFile]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=RadioFile)

    
    async def  update_status(self, file_id: int, new_status: ProcessingStatus) -> RadioFile:
        query = (
            update(RadioFile)
            .where(RadioFile.id == file_id)
            .values(status = new_status)
            .returning(RadioFile)
            )
    
        result = await self.session.execute(query)
        await self.session.flush()

        return result.scalar_one_or_none()
    
