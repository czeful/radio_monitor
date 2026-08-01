import pytest

from database.repositories.unknown_detection_repository import UnknownDetectionRepository
from database.enums import ProcessingStatus
from datetime import datetime , timedelta, timezone

#==========================================================
# get_pending()
#==========================================================

@pytest.mark.asyncio
async def test_get_pending_status_match(session, unknown_detection_factory):
    repo = UnknownDetectionRepository(session=session)

    unknown_detection_pending = await unknown_detection_factory(
        status = ProcessingStatus.PENDING
    ), 

    unknown_detection_pending_2 = await unknown_detection_factory(
        status = ProcessingStatus.PENDING
    ),

    unknown_detection_not_pending = await unknown_detection_factory(
        status = ProcessingStatus.FAILED
    )

    result = await repo.get_pending()
    assert len(result) == 2

@pytest.mark.asyncio
async def test_get_pending_status_limit(session, unknown_detection_factory):
    repo = UnknownDetectionRepository(session=session)

    unknown_detection_pending = await unknown_detection_factory(
        status = ProcessingStatus.PENDING
    ), 

    unknown_detection_pending_2 = await unknown_detection_factory(
        status = ProcessingStatus.PENDING
    ),

    unknown_detection_not_pending = await unknown_detection_factory(
        status = ProcessingStatus.FAILED
    )

    result = await repo.get_pending(limit=1)
    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_pending_status_no_match(session, unknown_detection_factory):
    repo = UnknownDetectionRepository(session=session)

    unknown_detection_pending = await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED
    ), 

    unknown_detection_pending_2 = await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED
    ),

    unknown_detection_not_pending = await unknown_detection_factory(
        status = ProcessingStatus.FAILED
    )

    result = await repo.get_pending()
    assert len(result) == 0


#===========================================================================
# mark_proccesed()
#============================================================================

@pytest.mark.asyncio
async def test_mark_proccesed_status_change_check(session, unknown_detection_factory):
    repo = UnknownDetectionRepository(session=session)

    unknown_detection_1 = await unknown_detection_factory(
        status = ProcessingStatus.PENDING
    )

    unknown_detection_1 = await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED
    )

    result = await repo.mark_processed(unknown_detection_id=unknown_detection_1.id , status=ProcessingStatus.COMPLETED)

    assert result is not None
    assert result.id == unknown_detection_1.id
    assert result.status == ProcessingStatus.COMPLETED

@pytest.mark.asyncio
async def test_mark_proccesed_not_empt_check(session, unknown_detection_factory):
    repo = UnknownDetectionRepository(session=session)

    unknown_detection_1 = await unknown_detection_factory(
        status = ProcessingStatus.PENDING
    ) 

    unknown_detection_1 = await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED
    )

    result = await repo.mark_processed(unknown_detection_id=67, status=ProcessingStatus.COMPLETED)

    assert result is None


#================================================================
# get_by_date()
#================================================================
start = datetime.strptime("2020-08-01 16:26:00", "%Y-%m-%d %H:%M:%S")
end = datetime.strptime("2027-08-01 16:26:15", "%Y-%m-%d %H:%M:%S")

@pytest.mark.asyncio
async def test_get_by_date(session, unknown_detection_factory):
    repo = UnknownDetectionRepository(session=session)

    unknown_detection_old = await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED,
        created_at = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=3)
    )

    unknown_detection_custom = await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED,
        created_at = datetime(2023, 1, 1 , 12 , 0, 0)
    )
    
    unknown_detection_real = await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED,
    )

    result = await repo.get_by_date(start_date=start, end_date=end)
    assert len(result) == 3
    assert result[0].id == unknown_detection_real.id
    assert result[1].id == unknown_detection_old.id
    assert result[2].id == unknown_detection_custom.id



@pytest.mark.asyncio
async def test_get_by_date_limit_check(session, unknown_detection_factory):
    repo = UnknownDetectionRepository(session=session)

    unknown_detection_old = await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED,
        created_at = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=3)
    )

    unknown_detection_custom = await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED,
        created_at = datetime(2023, 1, 1 , 12 , 0, 0)
    )
    
    unknown_detection_real = await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED,
    )

    result = await repo.get_by_date(start_date=start, end_date=end , limit=1)
    assert len(result) == 1


start_no_match = datetime.strptime("2000-08-01 16:26:00", "%Y-%m-%d %H:%M:%S")
end_no_match= datetime.strptime("2001-08-01 16:26:15", "%Y-%m-%d %H:%M:%S")


@pytest.mark.asyncio
async def test_get_by_date_no_match(session, unknown_detection_factory):
    repo = UnknownDetectionRepository(session=session)

    await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED,
        created_at = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=3)
    )

    await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED,
        created_at = datetime(2023, 1, 1 , 12 , 0, 0)
    )
    
    await unknown_detection_factory(
        status = ProcessingStatus.COMPLETED,
    )

    result = await repo.get_by_date(start_no_match, end_no_match)
    assert len(result) == 0
 

    

