import pytest
from database.repositories.artist_repository import ArtistRepository

@pytest.mark.asyncio
async def test_get_by_name(session):
    repo = ArtistRepository(session=session)
    artist = await repo.create(
        name = "Test",
    )

    result = await repo.get_by_name(artist.name)

    assert result[0] == artist
    assert len(result) == 1

@pytest.mark.asyncio
async def test_get_by_name_returns_all_artists_with_same_name(session):
    repo = ArtistRepository(session=session)

    artist = await repo.create(name="Test")
    artist_2 = await repo.create(name="Test")

    result = await repo.get_by_name("Test")

    assert len(result) == 2
    assert result[0] == artist
    assert result[1] == artist_2


@pytest.mark.asyncio
async def test_artist_exists_return_true(session):
    repo = ArtistRepository(session=session)

    await repo.create(name="Test")
    result = await repo.exists_by_name("Test")

    assert result is True


@pytest.mark.asyncio
async def test_artist_exists_return_false(session):
    repo = ArtistRepository(session=session)

    await repo.create(name="Test_1")
    result = await repo.exists_by_name("Test")

    assert result is False