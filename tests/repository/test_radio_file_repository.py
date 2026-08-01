import pytest

from database.models.radio_file import RadioFile
from database.repositories.radio_file_repository import RadioFileRepository
from database.enums import ProcessingStatus


#===============================================================
#  update_status()
#===============================================================

@pytest.mark.asyncio
async def test_update_status(session):
    repo = RadioFileRepository(session=session)

    radio_file = await repo.create(
        filename = "Test_file",
        duration = 120,
        filepath = "C/anelya/oralsh",
        status  = ProcessingStatus.PENDING
    )

    result = await repo.update_status(radio_file.id, ProcessingStatus.FAILED)

    assert result.status == ProcessingStatus.FAILED
    assert radio_file.id == result.id
    assert radio_file.filename == result.filename
    assert radio_file.duration == result.duration


@pytest.mark.asyncio
async def test_update_status_return_none(session):

    repo = RadioFileRepository(session=session)

    await repo.create(
        filename = "Test_file",
        duration = 120,
        filepath = "C/anelya/oralsh",
        status  = ProcessingStatus.PENDING
    )

    result = await repo.update_status(767676767, ProcessingStatus.FAILED)

    assert result is None
