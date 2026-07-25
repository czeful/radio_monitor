import pytest_asyncio
import asyncio
import sys

from sqlalchemy.ext.asyncio import AsyncSession

from database.models.base import Base


# Импорт всех моделей обязательно
import database.models.artist
import database.models.song
import database.models.detection
import database.models.fingerprint
import database.models.songs_artists
import database.models.audio_segment
import database.models.radio_file
import database.models.unknown_detection


from database.models.artist import Artist
from database.models.song import Song

from database.enums import MusicClass

from tests.test_database import (
    test_engine,
    TestingSessionLocal
)


# =====================================================
# Windows asyncio fix
# =====================================================

if sys.platform == "win32":

    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )



# =====================================================
# Create / Drop test tables
# =====================================================

@pytest_asyncio.fixture(
    scope="session",
    autouse=True
)
async def create_tables():

    async with test_engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.drop_all
        )

        await conn.run_sync(
            Base.metadata.create_all
        )


    yield


    async with test_engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.drop_all
        )


    await test_engine.dispose()



# =====================================================
# Database session
# =====================================================

@pytest_asyncio.fixture
async def session() -> AsyncSession:


    async with TestingSessionLocal() as session:


        yield session


        # rollback незакоммиченных изменений
        await session.rollback()



        # очистка данных после теста
        for table in reversed(
            Base.metadata.sorted_tables
        ):

            await session.execute(
                table.delete()
            )


        await session.commit()



# =====================================================
# Artist Factory
# =====================================================

@pytest_asyncio.fixture
async def artist_factory(session):

    async def create_artist(
        name: str = "Test Artist"
    ) -> Artist:


        artist = Artist(
            name=name
        )


        session.add(artist)

        await session.flush()


        return artist


    return create_artist



# =====================================================
# Song Factory
# =====================================================

@pytest_asyncio.fixture
async def song_factory(session):


    async def create_song(
        title: str = "Test Song",
        duration: int = 180,
        music_class: MusicClass = MusicClass.UNKNOWN,
        artists: list[Artist] | None = None
    ) -> Song:


        song = Song(
            title=title,
            duration=duration,
            music_class=music_class
        )


        if artists:

            song.artists.extend(
                artists
            )


        session.add(song)

        await session.flush()


        return song


    return create_song