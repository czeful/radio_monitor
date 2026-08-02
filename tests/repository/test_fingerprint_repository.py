import pytest

from database.repositories.fingerprint_repository import FingerPrintRepository


#=================================================================
#  get_song_by_fingerprint()
#=================================================================

@pytest.mark.asyncio
async def test_get_song_by_fingerprint_returns_matching_fingerprint(
    session,
    fingerprint_factory,
    song_factory,
    ):

    repo = FingerPrintRepository(session=session)
    song_first = await song_factory()
    song_second = await song_factory()

    fingerprint_for_first_song = await fingerprint_factory(
        song = song_first,
        hash = "123123123123123",
        offset = 1
    )

    await fingerprint_factory(
        song = song_second,
        hash = "2123123123123123",
        offset = 10,
    )

    result = await repo.get_song_by_fingerprint(fingerprint=fingerprint_for_first_song.hash)

    assert len(result) == 1
    assert result[0].hash == fingerprint_for_first_song.hash
    assert result[0].song_id == song_first.id

@pytest.mark.asyncio
async def test_get_song_by_fingerprint_collision(
    session,
    fingerprint_factory,
    song_factory,
    ):

    repo = FingerPrintRepository(session=session)
    song_first = await song_factory()
    song_second = await song_factory()

    fingerprint_for_first_song = await fingerprint_factory(
        song = song_first,
        hash = "123123123123123",
        offset = 1
    )

    fingerprint_for_second_song = await fingerprint_factory(
        song = song_second,
        hash = "123123123123123",
        offset = 10,
    )

    result = await repo.get_song_by_fingerprint(fingerprint=fingerprint_for_first_song.hash)

    assert len(result) == 2
    assert result[0].song_id == song_first.id
    assert result[1].song_id == song_second.id


@pytest.mark.asyncio
async def test_get_song_by_fingerprint_returns_no_matching_fingerprint(
    session,
    fingerprint_factory,
    song_factory,
    ):

    repo = FingerPrintRepository(session=session)
    song_first = await song_factory()
    song_second = await song_factory()

    await fingerprint_factory(
        song = song_first,
        hash = "123123123123123",
        offset = 1
    )

    await fingerprint_factory(
        song = song_second,
        hash = "2123123123123123",
        offset = 10,
    )

    result = await repo.get_song_by_fingerprint(fingerprint="67-67-67-67-67")

    assert len(result) == 0



#================================================================
# exists_fingerprint()
#================================================================
@pytest.mark.asyncio
async def test_exists_fingerprint_with_true_fingerprint(session, fingerprint_factory):
    repo = FingerPrintRepository(session=session)

    fingerprint_true_hash = await fingerprint_factory(
        hash = "123123123123123",
        offset = 1
    )

    await fingerprint_factory(
        hash = "2123123123123123",
        offset = 10,
    )

    result = await repo.exists_fingerprint(fingerprint=fingerprint_true_hash.hash)
    assert result == True

@pytest.mark.asyncio
async def test_exists_fingerprint_with_false_fingerprint(session, fingerprint_factory):
    repo = FingerPrintRepository(session=session)

    await fingerprint_factory(
        hash = "123123123123123",
        offset = 1
    )

    await fingerprint_factory(
        hash = "2123123123123123",
        offset = 10,
    )

    result = await repo.exists_fingerprint(fingerprint="67-67-67-67")
    assert result == False
    


