from pathlib import Path
from typing import List, Dict

from pydub import AudioSegment


class AudioChunker:
    """
    Разбивает большое аудио на небольшие фрагменты.

    Используется перед:
    - YAMNet
    - PANNs
    - CLAP
    - Whisper
    """

    def __init__(self, chunk_duration_seconds: int = 5):
        self.chunk_duration_seconds = chunk_duration_seconds

    def split_audio(
        self,
        audio_path: str,
        output_dir: str
    ) -> List[Dict]:
        """
        Разбивает аудио на чанки фиксированной длины.

        Parameters
        ----------
        audio_path : str
            Путь к WAV файлу.

        output_dir : str
            Куда сохранять чанки.

        Returns
        -------
        List[Dict]
            Метаданные всех чанков.
        """

        audio_file = Path(audio_path)

        if not audio_file.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_file}"
            )

        output_directory = Path(output_dir)
        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        print(f"[INFO] Loading audio: {audio_file}")

        audio = AudioSegment.from_wav(audio_file)

        total_duration_ms = len(audio)

        chunk_length_ms = (
            self.chunk_duration_seconds * 1000
        )

        chunks_metadata = []

        chunk_index = 0

        for start_ms in range(
            0,
            total_duration_ms,
            chunk_length_ms
        ):

            end_ms = min(
                start_ms + chunk_length_ms,
                total_duration_ms
            )

            chunk = audio[start_ms:end_ms]

            chunk_filename = (
                f"chunk_{chunk_index:06d}.wav"
            )

            chunk_path = (
                output_directory /
                chunk_filename
            )

            chunk.export(
                chunk_path,
                format="wav"
            )

            chunks_metadata.append(
                {
                    "chunk_id": chunk_index,
                    "start_time": round(
                        start_ms / 1000,
                        2
                    ),
                    "end_time": round(
                        end_ms / 1000,
                        2
                    ),
                    "duration": round(
                        (end_ms - start_ms) / 1000,
                        2
                    ),
                    "path": str(chunk_path)
                }
            )

            chunk_index += 1

        print(
            f"[SUCCESS] Created "
            f"{len(chunks_metadata)} chunks"
        )

        return chunks_metadata

    @staticmethod
    def seconds_to_timestamp(
        seconds: float
    ) -> str:
        """
        Конвертирует секунды в HH:MM:SS.
        """

        total_seconds = int(seconds)

        hours = total_seconds // 3600

        minutes = (
            total_seconds % 3600
        ) // 60

        secs = total_seconds % 60

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{secs:02d}"
        )