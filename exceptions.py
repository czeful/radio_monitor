from database.enums import MusicClass
from datetime import datetime

class BaseDomainExeption(Exception):
    pass


class SongAlreadyExistsError(BaseDomainExeption):
    def __init__(self, title:str, artist_ids: list[int]) -> None:
        self.title =title,
        self.artist_ids=artist_ids

        messasge = f"Song with title {title} and same artist alredy exists."
        super().__init__(messasge)


class ArtistNotFoundError(BaseDomainExeption):
    def __init__(self, artist_ids: list[int] | int) -> None:
        self.artist_ids = artist_ids

        message = f"missing artist ids [{artist_ids}]"
        super().__init__(message)

class SongNotFoundError(BaseDomainExeption):
    def __init__(self, list_ids: list[int] | int) -> None:

        message = f"missing ids, no songs with {list_ids} ids"
        super().__init__(message)

class DetectionNotFoundError(BaseDomainExeption):
    def __init__(self, list_ids: list[int] | int) -> None:

        message = f"missing ids, no detection with {list_ids} ids"
        super().__init__(message)

 
class IncorrectSongAtributsError(BaseDomainExeption):
    def __init__(self , title: str , music_class: MusicClass) -> None:

        message = f"atribite_1 = {title} and music_class = {music_class}is not None. You need only one Not None atribute"
        super().__init__(message)

class IncorrectDetectionAtributsError(BaseDomainExeption):

    def __init__(self , song_id: str , start_date:datetime, end_date:datetime) -> None:

        message = f"song_id = {song_id} and start_date = {start_date}i or end_date = {end_date} are not None. You need only one Not None atribute"
        super().__init__(message)

class UnknownSongDetectionError(BaseDomainExeption):
    def __init__(self):
        message = f"This detection without song_id. This is Unknown detecion"
        super().__init__(message) 