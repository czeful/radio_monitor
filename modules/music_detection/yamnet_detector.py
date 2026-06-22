from modules.music_detection.detector_interface import (
    DetectorInterface
)

from modules.music_detection.music_prediction import (
    MusicPrediction
)


class YamnetDetector(DetectorInterface):

    def predict(
        self,
        chunk_metadata: dict
    ) -> MusicPrediction:

        return MusicPrediction(
            chunk_id=chunk_metadata["chunk_id"],
            start_time=chunk_metadata["start_time"],
            end_time=chunk_metadata["end_time"],
            label="unknown",
            confidence=0.0
        )