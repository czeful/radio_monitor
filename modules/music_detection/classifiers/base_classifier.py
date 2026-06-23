from abc import ABC, abstractmethod

import numpy as np


class BaseAudioClassifier(ABC):

    @abstractmethod
    def predict(
        self,
        waveform: np.ndarray,
        sample_rate: int
    ) -> tuple[str, float]:
        """
        Returns:
            (label, confidence)
        """
        pass