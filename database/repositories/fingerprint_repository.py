from repositories.base_repository import BaseRepository
from typing import TYPE_CHECKING 
from models.fingerprint import FingerPrint
from sqlalchemy import select, delete, update, func, exists


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class FingerPrintRepository(BaseRepository[FingerPrint]): 
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=FingerPrint)
    
    """
        Мысли:
            Метод get_song_by_fingerprint - ищет песни с помошью fingerprint, однако нет гарантий того что 
            у нас не будет колизии и у нас в базе нет разынх песен с одинаковым fingerprint. В таком случает возвращяем
            список из song_id. Думаю это супер большая редкость, если на практике не оправдается будем возращать просто один id

        Thoughts:
            The get_song_by_fingerprint method searches for songs using fingerprints, but there's no guarantee that
            we won't have collisions and that we don't have different songs with the same fingerprint in our database. In this case, we return
            a list of song_ids. I think this is incredibly rare; if it doesn't work out in practice, we'll simply return a single ID.
            
    """
    async def get_song_by_fingerprint(self, fingerprint: str) -> list[int] | None:
        query = select(FingerPrint).where(FingerPrint.hush == fingerprint)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def exists(self, fingerprint: str) -> bool:
        query = select(exists().where(FingerPrint.hash == fingerprint))
        result  = await self.session.execute(query)
        return bool(result.scalar())    