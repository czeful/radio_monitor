from modules.music_detection.music_prediction import (
    MusicPrediction
)

from modules.music_detection.segment_merger import (
    SegmentMerger
)


def main():

    predictions = [

        MusicPrediction(
            0, 0, 5,
            "music",
            0.9
        ),

        MusicPrediction(
            1, 5, 10,
            "music",
            0.95
        ),

        MusicPrediction(
            2, 10, 15,
            "music",
            0.91
        ),

        MusicPrediction(
            3, 15, 20,
            "speech",
            0.98
        ),

        MusicPrediction(
            4, 20, 25,
            "speech",
            0.98
        ),

        MusicPrediction(
            5, 25, 30,
            "music",
            0.87
        ),

        MusicPrediction(
            6, 30, 35,
            "music",
            0.88
        )

    ]

    merger = SegmentMerger()

    segments = merger.merge(
        predictions
    )

    for segment in segments:
        print(segment)


if __name__ == "__main__":
    main()