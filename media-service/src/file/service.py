from typing import List

from src.file.repository import FileRepository
from src.file.schemas import FileCreateSchema, FileSchema


class FileService:
    @classmethod
    async def add(cls, file_model: FileCreateSchema) -> FileSchema:
        file_value = file_model.model_dump()
        db_file = await FileRepository.add(file_value)
        return FileSchema.model_validate(db_file)


    @classmethod
    async def get_files_from_media(cls, media_id: int) -> List[FileSchema]:
        db_file_seq = await FileRepository.get_on_media_id(media_id)
        return [FileSchema.model_validate(file) for file in db_file_seq]


