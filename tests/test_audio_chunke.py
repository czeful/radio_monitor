from modules.music_detection.audio_chunker import (
    AudioChunker
)


def main():
    print("Start to make chunks")

    chunker = AudioChunker(
        chunk_duration_seconds=5
    )

    chunks = chunker.split_audio(
        audio_path="data/processed/radio.wav",
        output_dir="data/chunks"
    )

    print()
    print("=== FIRST 10 CHUNKS ===")

    for chunk in chunks[:10]:

        print(
            f"{chunk['chunk_id']} | "
            f"{chunk['start_time']} - "
            f"{chunk['end_time']} | "
            f"{chunk['path']}"
        )


if __name__ == "__main__":
    main()