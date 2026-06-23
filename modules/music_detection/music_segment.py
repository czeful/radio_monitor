from dataclasses import dataclass


@dataclass
class MusicSegment:

    start_time: float

    end_time: float

    confidence: float