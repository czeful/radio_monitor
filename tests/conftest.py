import asyncio
import sys

import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from database.models import Base
from database.models.artist import Artist
from database.models.song import Song
from database.enums import MusicClass


from tests.test_database import create_test_engine


if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_test_engine()

    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE;"))
        await conn.execute(text("CREATE SCHEMA public;"))
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE;"))
        await conn.execute(text("CREATE SCHEMA public;"))

    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):

    connection = await engine.connect()

    transaction =  await connection.begin()

    SessionLocal = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        class_=AsyncSession,
        join_transaction_mode="create_savepoint",
    )

    async with SessionLocal() as session:
        await session.begin_nested()

        from sqlalchemy import event
        @event.listens_for(session.sync_session, "after_transaction_end")
        def restart_savepoint(sync_session, transaction_obj):
            if transaction_obj.nested and not transaction_obj._parent.nested:
                sync_session.begin_nested()
        yield session

        await transaction.rollback()
        await connection.close()

@pytest_asyncio.fixture
async def artist_factory(session):

    async def create_artist(name: str = "Test Artist") -> Artist:

        artist = Artist(name=name)
        session.add(artist)
        await session.flush()
        return artist

    return create_artist


@pytest_asyncio.fixture
async def song_factory(session):
    async def create_song(
        title: str = "Test Song",
        duration: int = 180,
        music_class: MusicClass = MusicClass.UNKNOWN,
        artists: list[Artist] | None = None,
    ) -> Song:

        song = Song(
            title=title,
            duration=duration,
            music_class=music_class,
        )

        if artists:
            song.artists.extend(artists)

        session.add(song)
        await session.flush()
        return song

    return create_song