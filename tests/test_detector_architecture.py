from modules.music_detection.classifiers.yamnet_detector import (
    YamnetDetector
)

from modules.music_detection.music_detector_service import (
    MusicDetectorService
)


def main():

    detector = YamnetDetector()

    service = MusicDetectorService(
        detector
    )

    chunks = [
        {
            "chunk_id": 1,
            "start_time": 0,
            "end_time": 5,
            "path": r"C:\Users\Bieber\Desktop\radio-monitor\data\chunks\chunk_000001.wav"
        }
    ]

    predictions = service.process_chunks(
        chunks
    ) 

    for prediction in predictions:
        print(prediction)


if __name__ == "__main__":
    main()