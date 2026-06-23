from pathlib import Path

import soundfile as sf
import numpy as np


class AudioLoader:

    @staticmethod
    def load_audio(
        audio_path: str
    ) -> tuple[np.ndarray, int]:

        path = Path(audio_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {path}"
            )

        waveform, sample_rate = sf.read(path)

        waveform = waveform.astype(
            np.float32
        )

        return waveform, sample_rate