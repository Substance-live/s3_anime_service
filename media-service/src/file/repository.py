from typing import Sequence

from sqlalchemy import select

from src.db import Session_maker
from src.file.models import FileOrm


class FileRepository:

    @classmethod
    async def add(cls, value: dict) -> FileOrm:
        async with Session_maker() as session:
            new_file = FileOrm(**value)
            session.add(new_file)
            await session.commit()
            await session.refresh(new_file)
            return new_file

    @classmethod
    async def get_on_media_id(cls, media_id: int) -> Sequence[FileOrm]:
        async with Session_maker() as session:
            query = select(FileOrm).where(FileOrm.media_id == media_id)
            ret = await session.scalars(query)

            return ret.all()


