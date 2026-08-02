import pytest 
from services.song_service import SongService


@pytest.mark.asyncio
async def test_create_song(session):
    service = SongService()

