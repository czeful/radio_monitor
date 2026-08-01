import pytest 
from database.repositories.detection_repository import DetectionRepository
from database.models.song import Song 
from database.models.audio_segment import AudioSegment
from database.enums import MatchType, DetectionStatus
from datetime import datetime , timedelta, timezone


start = datetime.strptime("2020-08-01 16:26:00", "%Y-%m-%d %H:%M:%S")
end = datetime.strptime("2027-08-01 16:26:15", "%Y-%m-%d %H:%M:%S")

#======================================================================= 
#   get_history()  
#========================================================================
@pytest.mark.asyncio
async def test_get_hisoty(session, detection_factory):
    repo = DetectionRepository(session=session)

    d1 = await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )
    d2 = await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )
    d3 = await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )

    history = await repo.get_history(10)

    assert len(history) == 3
    assert history[0] == d1
    assert history[1] == d2
    assert history[2] == d3

@pytest.mark.asyncio
async def test_get_history_limit(session, detection_factory):
    repo = DetectionRepository(session=session)

    await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )
    await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )
    await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )
    await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )
    await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )
    await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )

    history = await repo.get_history(3)

    assert len(history) == 3


@pytest.mark.asyncio
async def test_get_history_empt(session):
    repo = DetectionRepository(session=session)

    history = await repo.get_history(10)

    assert history == []



#======================================================================= 
#   get_by_song()  
#========================================================================

@pytest.mark.asyncio
async def test_get_by_song(
    session, 
    detection_factory,
    song_factory,
    ):
    repo = DetectionRepository(session=session)
    song_1 = await song_factory()

    d1 = await detection_factory(
        song = song_1,
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )
    d2 = await detection_factory(
        song = song_1,
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )
    d3 = await detection_factory(
        song = song_1, 
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )

    result = await repo.get_by_song(d1.song_id)

    assert len(result) == 3
    assert result[0] == d1
    assert result[1] == d2
    assert result[2] == d3


@pytest.mark.asyncio
async def test_get_by_song_check_on_different_song_id(
    session,
    detection_factory, song_factory
    ):
    repo = DetectionRepository(session=session)

    song_1 = await song_factory()
    song_2 = await song_factory()

    d1 = await detection_factory(
        song = song_1,
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )
    d2 = await detection_factory(
        song = song_2,
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )
    d3 = await detection_factory(
        song = song_2,
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )
    d4 = await detection_factory(
        song = song_1,
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )

    result = await repo.get_by_song(d1.song_id)

    assert len(result) == 2
    assert result[0] == d1
    assert result[1] == d4

@pytest.mark.asyncio
async def test_get_by_song_no_maches(session):
    repo = DetectionRepository(session=session)

    result = await repo.get_by_song(12)
    assert result == []

#======================================================================= 
#   get_by_date()  
#========================================================================

@pytest.mark.asyncio
async def test_get_by_date(session, detection_factory, song_factory):
    repo = DetectionRepository(session=session)

    song_1 = await song_factory()
    song_2 = await song_factory()

    detection_song_old = await detection_factory(
        song = song_1,
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
        created_at = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=3)
    )
    custom_detection = await detection_factory(
        song = song_1,
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
        created_at = datetime(2023, 1, 1 , 12 , 0, 0)
    )
    default_detection = await detection_factory(
        song = song_2,
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )

    detection_witout_song = await detection_factory(
        match_type = MatchType.ML_MODEL,
        status = DetectionStatus.NOT_FOUND,
    )


    result = await repo.get_by_date(start, end, song_1.id)
    assert len(result) == 2
    assert result[0] == detection_song_old
    assert result[1] == custom_detection
    assert result[0].created_at > result[1].created_at


@pytest.mark.asyncio
async def test_get_by_date_without_song_id(session, detection_factory):
    repo = DetectionRepository(session=session)
    
    detection_song_old = await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
        created_at = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=3)
    )
    custom_detection = await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
        created_at = datetime(2023, 1, 1 , 12 , 0, 0)
    )
    default_detection = await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND,
    )

    result = await repo.get_by_date(start, end)

    assert len(result) == 3
    assert result[0] == default_detection
    assert result[1] == detection_song_old
    assert result[2] == custom_detection


@pytest.mark.asyncio
async def test_get_by_date_with_none_return(session):
    repo = DetectionRepository(session=session)

    result = await repo.get_by_date(start, end)

    assert result == []


#=============================================================================
#   count_detections()
#===========================================================================
@pytest.mark.asyncio
async def test_count_detections_only_by_song_id(session, detection_factory, song_factory):
    repo = DetectionRepository(session=session) 
    song_1 = await song_factory()

    detection = [
        await detection_factory(
        song = song_1,
        match_type=MatchType.ML_MODEL,
        status=DetectionStatus.MATCHED
    )
    for _ in range(5)
    ]

    detection_with_another_status = await detection_factory(
        match_type = MatchType.FINGERPRINT,
        status = DetectionStatus.NOT_FOUND
    )
    detection_with_another_match_type = await detection_factory(
        match_type = MatchType.ML_MODEL,
        status = DetectionStatus.ERROR
    )


    result = await repo.count_detections(song_id=song_1.id)

    assert result == 5


@pytest.mark.asyncio
async def test_count_detections_only_by_match_type(session, detection_factory):
    repo = DetectionRepository(session=session) 
    detection = [
        await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.ERROR
    )
    for _ in range(5)
    ]

    detection_with_another_id = await detection_factory(
        match_type = MatchType.ML_MODEL,
        status = DetectionStatus.ERROR
    )
    detection_with_another_match_type = await detection_factory(
        match_type = MatchType.ML_MODEL,
        status = DetectionStatus.ERROR
    )


    result = await repo.count_detections(match_type=detection[1].match_type )

    assert result == 5


@pytest.mark.asyncio
async def test_count_detections_only_by_status(session, detection_factory):
    repo = DetectionRepository(session=session) 
    detection = [
        await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND
    )
    for _ in range(5)
    ]

    detection_with_another_status = await detection_factory(
        match_type = MatchType.FINGERPRINT,
        status = DetectionStatus.ERROR
    )

    result = await repo.count_detections(status=detection[0].status)

    assert result == 5

@pytest.mark.asyncio
async def test_count_detections_by_song_id_match_type(
    session, 
    detection_factory,
    song_factory,
    ):

    song_1 = await song_factory()
    repo = DetectionRepository(session=session) 
    detection = [
        await detection_factory(
        song = song_1,
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.NOT_FOUND
    )
    for _ in range(5)
    ]

    detection_with_another_match_type = await detection_factory(
        match_type = MatchType.ML_MODEL,
        status = DetectionStatus.ERROR
    )


    detection_with_another_song_id = await detection_factory(
        match_type = MatchType.FINGERPRINT,
        status = DetectionStatus.ERROR
    )

    result = await repo.count_detections(
        song_id=song_1.id,
        match_type=detection[0].match_type 
    )

    assert result == 5

@pytest.mark.asyncio
async def test_count_detections_by_song_id_and_status(
    session,
    detection_factory,
    song_factory
    ):


    song_1 = await song_factory()
    repo = DetectionRepository(session=session) 
    detection = [
        await detection_factory(
        song = song_1,
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.ERROR
    )
    for _ in range(5)
    ]

    detection_with_another_song_id = await detection_factory(
        match_type = MatchType.FINGERPRINT,
        status = DetectionStatus.ERROR
    )

    result = await repo.count_detections(
        song_id=song_1.id,
        status=detection[0].status
    )

    assert result == 5

@pytest.mark.asyncio
async def test_count_detections_by_status_and_match_type(
    session, 
    detection_factory
    ):

    repo = DetectionRepository(session=session) 
    detection = [
        await detection_factory(
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.ERROR
    )
    for _ in range(5)
    ]

    detection_with_another_status = await detection_factory(
        match_type = MatchType.FINGERPRINT,
        status = DetectionStatus.NOT_FOUND
    )
    detection_with_another_match_type = await detection_factory(
        match_type = MatchType.ML_MODEL,
        status = DetectionStatus.ERROR
    )

    result = await repo.count_detections(
        match_type=detection[0].match_type,
        status=detection[0].status
    )

    assert result == 5

@pytest.mark.asyncio
async def test_count_detections_by_song_status_and_match_type(
    session, 
    detection_factory,
    song_factory,
    ):

    repo = DetectionRepository(session=session) 
    song_1 = await song_factory()
    detection = [
        await detection_factory(
        song = song_1,
        match_type=MatchType.FINGERPRINT,
        status=DetectionStatus.ERROR
    )
    for _ in range(5)
    ]

    detection_with_another_status = await detection_factory(
        match_type = MatchType.FINGERPRINT,
        status = DetectionStatus.NOT_FOUND
    )
    detection_with_another_match_type = await detection_factory(
        match_type = MatchType.ML_MODEL,
        status = DetectionStatus.ERROR
    )

    result = await repo.count_detections(
        song_id=song_1.id,
        match_type=detection[0].match_type,
        status=detection[0].status
    )

    assert result == 5
