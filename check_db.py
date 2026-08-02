import asyncio

from tests.test_database import create_test_engine
from database.models.base import Base

import database.models.artist
import database.models.song
import database.models.detection
import database.models.fingerprint
import database.models.unknown_detection
import database.models.songs_artists
import database.models.audio_segment
import database.models.radio_file


async def main():
    engine = create_test_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


asyncio.run(main())