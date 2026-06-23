from modules.music_detection.detector_interface import (
    DetectorInterface
)

from modules.music_detection.music_prediction import (
    MusicPrediction
)

from modules.music_detection.audio_loader import (
    AudioLoader
)

from modules.music_detection.classifiers.dummy_classifier import (
    DummyClassifier
)


class YamnetDetector(
    DetectorInterface
):

    def __init__(self):

        self.classifier = (
            DummyClassifier()
        )

    def predict(
        self,
        chunk_metadata: dict
    ) -> MusicPrediction:

        waveform, sample_rate = (
            AudioLoader.load_audio(
                chunk_metadata["path"]
            )
        )

        label, confidence = (
            self.classifier.predict(
                waveform,
                sample_rate
            )
        )

        return MusicPrediction(
            chunk_id=chunk_metadata["chunk_id"],
            start_time=chunk_metadata["start_time"],
            end_time=chunk_metadata["end_time"],
            label=label,
            confidence=confidence
        )