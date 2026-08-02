import pytest 

from  database.repositories.base_repository import BaseRepository

from database.models.song import Song
from database.enums import MusicClass



@pytest.mark.asyncio
async def test_create(session):
    
    repo  = BaseRepository(
        session=session,
        model=Song
    )

    song = await repo.create(
        title="Test Song",
        duration=200, #sec
        music_class=MusicClass.FOREIGN
    )

    assert song.id is not None
    assert song.title == "Test Song"


@pytest.mark.asyncio
async def test_get_by_id(session):
    repo = BaseRepository(session=session, model=Song)
    song = await repo.create(
        title = "Imagine",
        duration= 180, #sec
        music_class = MusicClass.FOREIGN
    )

    result = await repo.get_by_id(
        song.id
    )
    
    assert result is not None
    assert result.id == song.id
    assert result.title == "Imagine"

@pytest.mark.asyncio
async def test_get_by_id_not_found(
    session
):

    repo = BaseRepository(
        session=session,
        model=Song
    )


    result = await repo.get_by_id(
        999999
    )


    assert result is None



@pytest.mark.asyncio
async def test_get_by_ids(
    session
):

    repo = BaseRepository(
        session=session,
        model=Song
    )


    song1 = await repo.create(
        title="Song 1",
        duration=100,
        music_class=MusicClass.KAZAKH
    )


    song2 = await repo.create(
        title="Song 2",
        duration=200,
        music_class=MusicClass.FOREIGN
    )


    result = await repo.get_by_ids(
        [
            song1.id,
            song2.id
        ]
    )


    assert len(result) == 2



@pytest.mark.asyncio
async def test_get_by_ids_empty(
    session
):

    repo = BaseRepository(
        session=session,
        model=Song
    )


    result = await repo.get_by_ids([])


    assert result == []



@pytest.mark.asyncio
async def test_get_all(
    session
):

    repo = BaseRepository(
        session=session,
        model=Song
    )


    await repo.create(
        title="Song 1"
    )

    await repo.create(
        title="Song 2"
    )

    await repo.create(
        title="Song 3"
    )


    result = await repo.get_all(
        limit=2
    )


    assert len(result) == 2



@pytest.mark.asyncio
async def test_update(
    session
):

    repo = BaseRepository(
        session=session,
        model=Song
    )


    song = await repo.create(
        title="Old title",
        duration=100
    )


    updated_song = await repo.update(
        song.id,
        title="New title"
    )


    assert updated_song is not None
    assert updated_song.title == "New title"



@pytest.mark.asyncio
async def test_update_without_changes(
    session
):

    repo = BaseRepository(
        session=session,
        model=Song
    )


    song = await repo.create(
        title="Same"
    )


    result = await repo.update(
        song.id
    )


    assert result.title == "Same"



@pytest.mark.asyncio
async def test_exists(
    session
):

    repo = BaseRepository(
        session=session,
        model=Song
    )


    song = await repo.create(
        title="Exists"
    )


    result = await repo.exists(
        song.id
    )


    assert result is True



@pytest.mark.asyncio
async def test_exists_false(
    session
):

    repo = BaseRepository(
        session=session,
        model=Song
    )


    result = await repo.exists(
        999999
    )


    assert result is False



@pytest.mark.asyncio
async def test_count(
    session
):

    repo = BaseRepository(
        session=session,
        model=Song
    )


    await repo.create(
        title="Song 1"
    )

    await repo.create(
        title="Song 2"
    )


    count = await repo.count()


    assert count == 2



@pytest.mark.asyncio
async def test_delete(
    session
):

    repo = BaseRepository(
        session=session,
        model=Song
    )


    song = await repo.create(
        title="Delete me"
    )


    await repo.delete(song)


    await session.flush()


    result = await repo.get_by_id(
        song.id
    )


    assert result is None



@pytest.mark.asyncio
async def test_delete_by_id(
    session
):

    repo = BaseRepository(
        session=session,
        model=Song
    )


    song = await repo.create(
        title="Delete by id"
    )


    await repo.delete_by_id(
        song.id
    )


    await session.flush()

    result = await repo.get_by_id(
        song.id
    )


    assert result is None