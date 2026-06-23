from modules.music_detection.classifiers.base_classifier import (
    BaseAudioClassifier
)


class DummyClassifier(
    BaseAudioClassifier
):

    def predict(
        self,
        waveform,
        sample_rate
    ):

        duration = (
            len(waveform)
            / sample_rate
        )

        if duration >= 5:
            return (
                "music",
                0.5
            )

        return (
            "other",
            0.1
        )