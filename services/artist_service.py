from database.models.artist import Artist
from exceptions import ArtistNotFoundError
from database.repositories.artist_repository import ArtistRepository
class ArtistService:
    def __init__(self, artist_repository:ArtistRepository):
        self.artist_repository = artist_repository


    async def get_by_ids(
            self,
            artist_ids: list[int]
    ) -> list[Artist]:

        artist = await self.artist_repository.get_by_id(artist_ids)

        if len(artist) != len(artist_ids):
            raise ArtistNotFoundError(artist_ids=artist_ids)
        return artist

    async def create_artist(
            self, 
            name: str,
        ) -> Artist:

        """
        Тут ограничение по имиени, созадть нового арстиа с уже сущетсвующем именем нельзя
        хотя по сути до этого логику прописывал под то, что бы можно было создавать артистов с одиноквыми 
        именами
        """

      #  exists_artist = await self.artist_repository.exists_by_name(artist_name=name)

      # if exists_artist is False:
      #      raise ValueError(
      #         f"Artist with same name exists"
      #      )

        new_artist = await self.artist_repository.create(name=name)
        return new_artist

    async def get_all_artists(
            self,
            limit: int,
            offset: int
    ) -> list[Artist]:

        artist_list = await self.artist_repository(limit=limit, offset=offset)


        return artist_list 

    async def update_artist_name(
            self,
            new_name: str,
            artist_id: int,
        ) -> Artist:

        artist_exists = await self.artist_repository.exists(object_id=artist_id)

        if artist_exists:
            updated_artist = await self.artist_repository.update(object_id=artist_id, name=new_name)

        else:
            raise ArtistNotFoundError(artist_ids=artist_id)

        return updated_artist

    async def delete_artist(
            self, 
            artist_id: int
    ) -> None:

        artist_exists = await self.artist_repository.exists(object_id=artist_id)

        if artist_exists:
            updated_artist = await self.artist_repository.delete_by_id(object_id=artist_id)
        else:
            raise ArtistNotFoundError(artist_ids=artist_id)

        return updated_artist