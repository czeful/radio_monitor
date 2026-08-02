from database.repositories.song_repository import SongRepository
from database.models.song import Song
from services.artist_service import ArtistService
from database.enums import MusicClass 
from exceptions import SongAlreadyExistsError, SongNotFoundError, IncorrectAtributsError

class SongService:

    def __init__(self, song_repository: SongRepository, artist_service: ArtistService):
        self.repository = song_repository
        self.artist_service= artist_service


    async def create_song(
            self, 
            title: str,
            duration: int, 
            artist_ids: list[int], 
            music_class: MusicClass     #TODO: Нужно в будущем это убрать, и заменить на MusicClasssificationService
            )-> Song:

        
        artists = await self.artist_service.get_by_ids(artist_ids=artist_ids)
        
        exists_song = await self.repository.exists_by_title_and_artists(
            title=title,
            artist_ids=artist_ids
            )
        
        if exists_song:
            raise SongAlreadyExistsError(
                title=title,
                artis_ids=artist_ids
                )

        song = await self.repository.create(
            title = title,
            duration = duration, 
            artists = artists,
            music_class = music_class
        )
        return song

    async def get_songs_by_ids(
        self, 
        song_ids: list[int]
    ) -> list[Song]:
        result = await self.repository.get_by_ids(list_ids=song_ids)

        unique_ids = set(song_ids)

        if len(result) != len(unique_ids):
            raise SongNotFoundError(list_ids=song_ids)
        
        return result


        """
        у данного метода есть проблемаЮ нельзя одновременно получить selct и по title и по class,
        тоесть обязательно нужно выбрать что то из двух или вообще ничего не выбирать что бы было 
        сортировка по get_all(). В будущем если нужна будет сортировка и по title и по class, тогда
        напишу новый метод в репозитоории, но пока остаылю так в надежде что этого фунуционала достаточно
        SIX - SEVEN
        """
    async def get_all_songs(
            self,
            limit: int,
            offset: int,
            title: str | None = None,
            music_class: MusicClass | None = None
        ) -> list[Song]:

        """ You can chose only title or music_class. You cant choose title and music_class"""

        if title is not None:
            result = await self.repository.get_by_title(title=title, limit=limit, offset=offset)
        if title is not None and music_class is not None:
            raise IncorrectAtributsError(title=title, music_class=music_class)
        elif music_class is not None:
            result = await self.repository.get_by_class(music_class=music_class, limit=limit, offset=offset)
        else:
            result = await self.repository.get_all(limit=limit, offset=offset)

        return result

    async def update_music_class(
            self,
            song_id:int,
            new_music_class: MusicClass,
        ) -> Song:

        song_exists = await self.repository.exists(object_id=song_id)

        if song_exists is False:
            raise SongNotFoundError(list_ids=song_id)

        updated_song = await self.repository.update(object_id=song_id, music_class=new_music_class)

        return updated_song
    
    async def delete_song(
            self,
            song_id: int,
        ) -> None:

        song_exists = await self.repository.exists(object_id=song_id)

        if song_exists is False:
            raise SongNotFoundError(list_ids=song_id)

        song_delete = await self.repository.delete_by_id(object_id=song_id)

        return song_delete



        
