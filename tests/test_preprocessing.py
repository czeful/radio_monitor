from modules.preprocessing.audio_preprocessor import AudioPreprocessor 

def main():

    preprocessor = AudioPreprocessor()

    processed_file = preprocessor.preprocess(
        input_path="data/input/radio_1.mp3",
        output_path="data/processed/radio.wav"
    )

    info = preprocessor.get_audio_info(
        processed_file
    )

    print()
    print("=== AUDIO INFO ===")

    for key, value in info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()