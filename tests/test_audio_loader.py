from modules.music_detection.audio_loader import (
    AudioLoader
)


def main():

    waveform, sample_rate = (
        AudioLoader.load_audio(
            "data/chunks/chunk_000000.wav"
        )
    )

    print(
        "Waveform shape:",
        waveform.shape
    )

    print(
        "Sample rate:",
        sample_rate
    )


if __name__ == "__main__":
    main()