from enum import StrEnum


class MediaStatus(StrEnum):
    pending = "pending"
    uploaded = "uploaded"
    failed = "failed"
    confirmed = "confirmed"
