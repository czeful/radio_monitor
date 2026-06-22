from pathlib import Path
from pydub import AudioSegment


class AudioPreprocessor:
    """
    Приводит любое входное аудио к единому формату.

    Целевой формат:

    - WAV
    - Mono
    - 16 kHz
    - 16 bit PCM

    Такой формат будет использоваться всеми
    последующими AI-модулями проекта.
    """

    TARGET_SAMPLE_RATE = 16000
    TARGET_CHANNELS = 1
    TARGET_SAMPLE_WIDTH = 2  # 16-bit

    def __init__(self):
        pass

    def preprocess(
        self,
        input_path: str,
        output_path: str
    ) -> Path:
        """
        Конвертирует аудио в целевой формат.

        Parameters
        ----------
        input_path : str
            Путь к исходному файлу.

        output_path : str
            Куда сохранить результат.

        Returns
        -------
        Path
            Путь к обработанному файлу.
        """

        input_file = Path(input_path)

        if not input_file.exists():
            raise FileNotFoundError(
                f"File not found: {input_file}"
            )

        print(f"[INFO] Loading: {input_file}")

        audio = AudioSegment.from_file(input_file)

        audio = audio.set_frame_rate(
            self.TARGET_SAMPLE_RATE
        )

        audio = audio.set_channels(
            self.TARGET_CHANNELS
        )

        audio = audio.set_sample_width(
            self.TARGET_SAMPLE_WIDTH
        )

        output_file = Path(output_path)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        audio.export(
            output_file,
            format="wav"
        )

        print(
            "[SUCCESS] Audio preprocessed:"
            f" {output_file}"
        )

        return output_file

    def get_audio_info(
        self,
        audio_path: str
    ) -> dict:
        """
        Возвращает информацию об аудио.
        """

        audio = AudioSegment.from_file(audio_path)

        duration_seconds = len(audio) / 1000

        return {
            "duration_seconds": round(duration_seconds, 2),
            "sample_rate": audio.frame_rate,
            "channels": audio.channels,
            "sample_width_bytes": audio.sample_width
        }
        