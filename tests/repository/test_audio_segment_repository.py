import pytest

from database.repositories.audio_segment_repository import AudioSegmentRepository
from database.models.audio_segment import AudioSegment
from database.models.radio_file import RadioFile
from database.enums import ProcessingStatus
from sqlalchemy import select

#===========================================================
# delete_old_segments() 
#===========================================================

@pytest.mark.asyncio
async def test_delete_old_segment(session, radio_file_factory, audio_segment_factory):
    repo = AudioSegmentRepository(session=session)
    radio_file = await radio_file_factory(
        status = ProcessingStatus.COMPLETED
    )

    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 0,
        end_time = 15,
    )

    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 15,
        end_time = 30,
    )

    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 30,
        end_time = 35,
    )    

    result = await repo.delete_old_segments(radio_file.id)

    assert  result is not None
    assert result == 3

    delete_check = await session.execute(
        select(AudioSegment)
        .where(AudioSegment.radio_file_id == radio_file.id)
    )

    segment = delete_check.scalars().all()

    assert len(segment) == 0



@pytest.mark.asyncio
async def test_delete_old_segments_no_complate(session, radio_file_factory, audio_segment_factory):

    repo = AudioSegmentRepository(session=session)
    radio_file = await radio_file_factory(
        status = ProcessingStatus.PENDING
    )

    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 0,
        end_time = 15,
    )

    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 15,
        end_time = 30,
    )

    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 30,
        end_time = 35,
    )    

    result = await repo.delete_old_segments(radio_file_id=radio_file.id)

    assert result == 0
    assert result is not None


    # Check the current obj at database
    delete_check = await session.execute(
        select(AudioSegment)
    )
    segments =  delete_check.scalars().all()
    assert len(segments) == 3
    assert result is not None


@pytest.mark.asyncio
async def test_delete_old_segments_with_no_match_redio_id(session, radio_file_factory , audio_segment_factory):
    repo = AudioSegmentRepository(session)

    radio_file = await radio_file_factory(
        status = ProcessingStatus.COMPLETED
    )
    
    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 0,
        end_time = 15,
    )

    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 15,
        end_time = 30,
    )

    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 30,
        end_time = 35,
    )    


    result = await repo.delete_old_segments(radio_file_id=radio_file.id + 10)

    assert result == 0
    assert result is not None 


#===========================================================
# get_by_radio_file_id() 
#===========================================================    

@pytest.mark.asyncio
async def test_get_by_radio_file_id(session, radio_file_factory, audio_segment_factory):

    repo = AudioSegmentRepository(session)

    radio_file = await radio_file_factory(
        status = ProcessingStatus.COMPLETED
    )
    
    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 0,
        end_time = 15,
    )

    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 15,
        end_time = 30,
    )

    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 30,
        end_time = 35,
    )    

    result = await repo.get_by_radio_file_id(radio_file_id=radio_file.id)

    assert len(result) == 3
    assert result is not None
    query = await session.execute(select(AudioSegment).where(AudioSegment.radio_file_id==radio_file.id).order_by(AudioSegment.id))
    result_check = query.scalars().all()

    for index in range(len(result)):
      assert result[index] == result_check[index]


@pytest.mark.asyncio
async def test_get_by_radio_file_no_matches(session, radio_file_factory, audio_segment_factory):
    repo = AudioSegmentRepository(session)

    radio_file = await radio_file_factory(
        status = ProcessingStatus.COMPLETED
    )
    
    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 0,
        end_time = 15,
    )

    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 15,
        end_time = 30,
    )

    await audio_segment_factory(
        radio_file_id = radio_file.id,
        start_time = 30,
        end_time = 35,
    )    

    result = await repo.get_by_radio_file_id(radio_file_id=radio_file.id + 10)

    assert len(result) == 0
