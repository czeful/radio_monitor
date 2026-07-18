from enum import Enum 


class MusicClass(Enum):
    KAZAKH = "kazakh"
    SOVIET = "soviet"
    FOREIGN = "foreign"
    UNKNOWN = "unknown"


class ProcessingStatus(Enum):
    PENDING = 1,
    PROCESSING = 2
    COMPLETED = 3,
    FAILED = 4

class DetectionStatus(Enum):
    MATCHED  = 1,
    NOT_FOUND = 2,
    ERROR = 3, 


class MatchType(Enum):
    FINGERPRINT = 1,
    ML_MODEL = 2,
    MANUAL = 3,