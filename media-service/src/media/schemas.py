from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.media.enum.media_status import MediaStatus


class MediaSchema(BaseModel):
    id: int
    s3_key: str
    status: MediaStatus
    expires_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class MediaCreateSchema(BaseModel):
    s3_key: str
    status: MediaStatus
    expires_at: datetime | None = None

