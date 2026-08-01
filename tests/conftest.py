import asyncio
import sys

from datetime import datetime
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)



from typing import Any

from database.models import Base
from database.models.artist import Artist
from database.models.song import Song
from database.enums import MusicClass
from database.enums import ProcessingStatus
from database.models import RadioFile
from database.models import AudioSegment
from database.enums import MatchType
from database.enums import DetectionStatus
from database.models.detection import Detection
from database.models.fingerprint import FingerPrint
from database.models.unknown_detection import UnknownDetection
from tests.test_database import create_test_engine


if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

MISSING  = object()


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


@pytest_asyncio.fixture
async def radio_file_factory(session):
    async def create_radio_file(
            filename: str = "test.mp3",
            filepath: str = "/tmp/test.mp3",
            status: ProcessingStatus = ProcessingStatus.PROCESSING,
            duration: int | None = None,
    ):
        radio_file = RadioFile(
            filename=filename,
            filepath=filepath,
            status=status,
            duration=duration,
        )

        session.add(radio_file)
        await session.flush()
        return radio_file
    return create_radio_file    

@pytest_asyncio.fixture
async def audio_segment_factory(session, radio_file_factory):
    async def create_audio_segment(
            file_path: str = "segment/anelya/oralsh",
            start_time: float = 1.4,
            end_time: float = 21.3,
            confidence: float = 0.98,
            radio_file: RadioFile | None = None,
            radio_file_id: int | Any = MISSING
        ):

        if radio_file is not None:
            radio_file_id = radio_file.id
        elif radio_file_id  is MISSING:
            radio_file = await radio_file_factory()
            radio_file_id = radio_file.id

        audio_segment = AudioSegment(
            start_time = start_time,
            end_time = end_time,
            file_path = file_path,
            confidence = confidence,
            radio_file_id = radio_file_id
        )



        session.add(audio_segment)
        await session.flush()
        return audio_segment
    return create_audio_segment

@pytest_asyncio.fixture
async def detection_factory(session, song_factory, audio_segment_factory ):
    async def create_detection(
            *,
            song: Song | None = None,
            song_id: int | None | Any = MISSING,
            audio_segment: AudioSegment | None = None,
            audio_segment_id: int | None = None,
            match_type: MatchType | None = None,
            status: DetectionStatus | None = None,
            confidence: float = 0.99,
            created_at: datetime | None = None 
    ) -> Detection:

        if song is not None:
            song_id = song.id
        elif song_id is MISSING:
            song = await song_factory()
            song_id = song.id

        if audio_segment is not None:
            audio_segment_id = audio_segment.id
        elif audio_segment_id is None:
            audio_segment = await audio_segment_factory()
            audio_segment_id = audio_segment.id


        kwargs = {
            "song_id": song_id,
            "audio_segment_id": audio_segment_id,
            "match_type": match_type,
            "status": status,
            "confidence": confidence,
        }

        if created_at is not None:
            kwargs["created_at"] = created_at
        
        detection = Detection(**kwargs)

        session.add(detection)
        await session.flush()
        return detection 
    
    return create_detection


@pytest_asyncio.fixture
async def fingerprint_factory(session, song_factory):
    async def create_fingerprint(
        song: Song | None = None,
        song_id: int | None | Any = MISSING,
        hash: str = "test_hash",
        offset: int = "0"
    ) -> FingerPrint:
        
        if song is not None:
            song_id = song.id
        elif song_id is MISSING:
            song = await song_factory()
            song_id = song.id

        fingerprint = FingerPrint(
            song_id = song_id,
             hash = hash,
             offset = offset,
        )
        session.add(fingerprint)
        await session.flush()
        return fingerprint 
    return create_fingerprint

@pytest_asyncio.fixture
async def unknown_detection_factory(session, song_factory, audio_segment_factory):
    async def create_unknown_detection(
            *,
            song: Song | None = None,
            song_id : int | None | Any = MISSING,
            audio_segment: AudioSegment | None = None,
            timestamp: datetime = datetime.now(),
            fingerprint: str = "test_fingerprint",
            audio_segment_id: int | None | Any = MISSING,
            status: ProcessingStatus = ProcessingStatus.PENDING, 
            audio_fragment_path: str = "test_path",
            classification_result: dict | None = None,
            created_at: datetime | None = None
    )-> UnknownDetection:

        if classification_result is None:
            classification_result = {"test": "test"}
        
        if song is not None:
            song_id = song.id
        elif song_id is MISSING:
            song = await song_factory()
            song_id = song.id

        if audio_segment is not None:
            audio_segment_id = audio_segment.id
        elif audio_segment_id is MISSING:
            audio_segment = await audio_segment_factory()
            audio_segment_id = audio_segment.id

        unknown_detection = UnknownDetection(
            song_id = song_id, 
            audio_segment_id = audio_segment_id,
            status = status,
            fingerprint = fingerprint,
            timestamp = timestamp,
            audio_fragment_path = audio_fragment_path,
            classification_result = classification_result,
            created_at = created_at
        )

        session.add(unknown_detection)
        await session.flush()
        return unknown_detection
    return create_unknown_detection

        