from datetime import datetime

from src.media.enum.media_status import MediaStatus
from src.media.repository import MediaRepository
from src.media.schemas import MediaSchema, MediaCreateSchema


class MediaService:
    @classmethod
    async def add(cls, media_model: MediaCreateSchema) -> MediaSchema:
        media_value = media_model.model_dump()
        db_media = await MediaRepository.add(media_value)
        return MediaSchema.model_validate(db_media)

    @classmethod
    async def get(cls, media_id: int) -> MediaSchema:
        db_media = await MediaRepository.get(media_id)
        if db_media is None:
            raise IndexError(f"media_id: {media_id} doen't exist")
        return MediaSchema.model_validate(db_media)

    @classmethod
    async def update_state(cls, media_id: int, new_state: MediaStatus) -> int:
        return await MediaRepository.update(media_id, {"status": new_state})

    @classmethod
    async def update_upload_expire_time(cls, media_id: int, new_time: datetime) -> int:
        return await MediaRepository.update(media_id, {"upload_expires_at": new_time})

    @classmethod
    async def update_download_expire_time(cls, media_id: int, new_time: datetime) -> int:
        return await MediaRepository.update(media_id, {"download_expires_at": new_time})
