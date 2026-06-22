from modules.music_detection.detector_interface import (
    DetectorInterface
)


class MusicDetectorService:

    def __init__(
        self,
        detector: DetectorInterface
    ):
        self.detector = detector

    def process_chunks(
        self,
        chunks_metadata: list
    ):

        predictions = []

        for chunk in chunks_metadata:

            prediction = self.detector.predict(
                chunk
            )

            predictions.append(
                prediction
            )

        return predictions