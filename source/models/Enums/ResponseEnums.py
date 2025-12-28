from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_INVALID = "Unsupported file type."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit."
    FILE_VALID = "File is valid."