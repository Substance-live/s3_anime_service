from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FileSchema(BaseModel):
    id: int
    media_id: int
    file_name: str
    s3_key: str
    content_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FileCreateSchema(BaseModel):
    media_id: int
    file_name: str
    s3_key: str
    content_type: str
    created_at: datetime
