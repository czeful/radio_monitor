import pytest

from database.models.song import Song
from database.repositories.song_repository import SongRepository
from database.enums import MusicClass



#======================================================================
                        # get_by_title()
#======================================================================

@pytest.mark.asyncio
async def test_get_by_title(session):
    repo = SongRepository(session=session)

    song = await repo.create(
        title = "anelya_qaidasyn",
        duration = 120,
        music_class = MusicClass.KAZAKH
    )

    result = await repo.get_by_title(song.title)

    assert result[0] == song
    assert len(result) == 1

@pytest.mark.asyncio
async def test_get_by_title_return_all_song_with_same_title(session):
    repo = SongRepository(session=session)

    song = await repo.create(
        title = "anelya_qaidasyn",
        duration = 120,
        music_class = MusicClass.KAZAKH        
    )

    song_2 = await repo.create(
        title = "anelya_qaidasyn",
        duration = 110,
        music_class = MusicClass.FOREIGN        
    )

    result = await repo.get_by_title("anelya_qaidasyn")

    assert len(result) == 2
    assert result[0] == song
    assert result[1] == song_2


@pytest.mark.asyncio
async def test_get_by_title_empty_result(session):

    repo = SongRepository(session=session)

    song = await repo.create(
        title = "anelya_qaidasyn",
        duration = 120,
        music_class = MusicClass.KAZAKH        
    )

    result = await repo.get_by_title("anelya_oralsh")

    assert len(result) == 0



#======================================================================
                        # get_by_class()
#======================================================================
@pytest.mark.asyncio
async def test_get_by_class(session):
    repo = SongRepository(session=session)

    song = await repo.create(
        title = "anelya_qaidasyn",
        duration = 120,
        music_class = MusicClass.KAZAKH        
    )

    result = await repo.get_by_class(MusicClass.KAZAKH)

    assert result[0] == song
    assert len(result) == 1

@pytest.mark.asyncio
async def test_get_by_class_with_all_same_classes(session):
    repo = SongRepository(session=session)

    song = await repo.create(
        title = "anelya_qaidasyn",
        duration = 120,
        music_class = MusicClass.KAZAKH        
    )

    song_2 = await repo.create(
        title = "anelya_oralsh",
        duration = 110,
        music_class = MusicClass.KAZAKH       
    )


    result = await repo.get_by_class(MusicClass.KAZAKH)

    assert len(result) == 2
    assert result[0] == song
    assert result[1] == song_2


@pytest.mark.asyncio
async def test_get_by_class_empty_result(session):

    repo = SongRepository(session=session)

    await repo.create(
        title = "anelya_qaidasyn",
        duration = 120,
        music_class = MusicClass.KAZAKH        
    )

    result = await repo.get_by_title("anelya_oralsh")

    assert len(result) == 0

#==============================================================
#                        exists_by_title()
#==============================================================

@pytest.mark.asyncio
async def test_exist_by_title_result_true(session):
    repo = SongRepository(session=session)

    await repo.create(
        title = "anelya_oralsh",
        duration = 110,
        music_class = MusicClass.KAZAKH             
    )

    result = await repo.exists_by_title("anelya_oralsh")

    assert result is True

@pytest.mark.asyncio
async def test_exist_by_title_result_false(session):
    repo = SongRepository(session=session)

    await repo.create(
        title = "anelya_oralsh",
        duration = 110,
        music_class = MusicClass.FOREIGN       
    )

    result = await repo.exists_by_title("Arman")

    assert result == False