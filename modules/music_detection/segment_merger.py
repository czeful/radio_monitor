from typing import List

from modules.music_detection.music_prediction import (
    MusicPrediction
)

from modules.music_detection.music_segment import (
    MusicSegment
)


class SegmentMerger:

    def merge(
        self,
        predictions: List[MusicPrediction]
    ) -> List[MusicSegment]:

        segments = []

        current_segment = None

        for prediction in predictions:

            if prediction.label != "music":

                if current_segment:

                    segments.append(
                        current_segment
                    )

                    current_segment = None

                continue

            if current_segment is None:

                current_segment = MusicSegment(
                    start_time=prediction.start_time,
                    end_time=prediction.end_time,
                    confidence=prediction.confidence
                )

            else:

                current_segment.end_time = (
                    prediction.end_time
                )

                current_segment.confidence = max(
                    current_segment.confidence,
                    prediction.confidence
                )

        if current_segment:

            segments.append(
                current_segment
            )

        return segments