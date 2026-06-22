from dataclasses import dataclass


@dataclass
class MusicPrediction:

    chunk_id: int

    start_time: float

    end_time: float

    label: str

    confidence: float