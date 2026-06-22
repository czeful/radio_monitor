from abc import ABC, abstractmethod

from modules.music_detection.music_prediction import (
    MusicPrediction
)


class DetectorInterface(ABC):

    @abstractmethod
    def predict(
        self,
        chunk_metadata: dict
    ) -> MusicPrediction:
        pass