from database.repositories.detection_repository import DetectionRepository
from database.models.detection import Detection
from database.enums import MusicClass , MatchType, DetectionStatus
from exceptions import UnknownSongDetectionError, IncorrectDetectionAtributsError, DetectionNotFoundError, SongNotFoundError
from datetime import datetime

class DetectionService:
    def __init__(self, detection_repository: DetectionRepository):
        self.detection_repository = detection_repository

    async def register_detection(
            self,
            song_id: int | None,
            audio_segment_id: int,
            match_type: MatchType,
            status: DetectionStatus,
            confidence: float,
        ) -> Detection:

        if song_id is None:

            new_detecion = await self.detection_repository.create(
                song_id = song_id, 
                audio_segment_id = audio_segment_id,
                match_type = match_type, 
                status = status,
                confidence = confidence
            )
        else:
            raise UnknownSongDetectionError()
        return new_detecion

    async def get_detection_history(
            self,
            limit: int,
            offset: int,
            song_id: int | None = None,
            start_date: datetime | None = None, 
            end_date: datetime | None = None,
    ) -> list[Detection]:

        if song_id is not None:
            result = await self.detection_repository.get_by_song(
                song_id=song_id,
                limit=limit,
                offset=offset
                )
            
        if song_id is not None and (start_date or end_date):
            raise IncorrectDetectionAtributsError(
                song_id=song_id,
                start_date=start_date,
                end_date=end_date
                )
        
        if start_date and end_date is not None:
            result = await self.detection_repository.get_by_date(
                start_date=start_date,
                end_date=end_date,
                limit=limit,
                offset=offset
                )
        return await self.detection_repository.get_history(
        limit=limit,
        offset=offset,
        )

    async def get_detection_statistics(
        self,
        song_id: int | None = None,
        match_type: MatchType | None = None,
        status: DetectionStatus | None = None,
    ) -> int:
        return await self.detection_repository.count_detections(
            song_id=song_id,
            match_type=match_type,
            status=status,
        )


    async def update_detecion_status(
         self, 
         detection_id: int,
         new_status: DetectionStatus,    
    ) -> Detection:

        exists_detection = await self.detection_repository.exists(object_id=detection_id)

        if exists_detection:
            update_detecion = await self.detection_repository.update(
                object_id=detection_id,
                status=new_status
                )
        else:
            raise DetectionNotFoundError(list_ids=detection_id)

        return update_detecion

    async def match_detection(
        self,
        detection_id: int,
        song_id: int,
        confidence: float,
        match_type: MatchType
    ) -> Detection:

        detection = await self.repository.get_by_id(
            object_id=detection_id
        )

        if detection is None:
            raise DetectionNotFoundError(
                detection_id=detection_id
            )

        song = await self.song_service.get_song_by_id(
            song_id=song_id
        )

        if song is None:
            raise SongNotFoundError(
                song_id=song_id
            )

        if detection.status == DetectionStatus.MATCHED:
            raise Exception(
                "Detection already matched"
            )

        updated_detection = await self.repository.update(
            object_id=detection_id,
            song_id=song_id,
            confidence=confidence,
            match_type=match_type,
            status=DetectionStatus.MATCHED
        )


        return updated_detection
    

