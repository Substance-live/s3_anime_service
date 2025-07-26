from sqlalchemy import update

from src.db import Session_maker
from src.media.models import MediaOrm


class MediaRepository:

    @classmethod
    async def add(cls, value: dict) -> MediaOrm:
        async with Session_maker() as session:
            new_media = MediaOrm(**value)
            session.add(new_media)
            await session.commit()
            await session.refresh(new_media)
            return new_media

    @classmethod
    async def get(cls, value_id: int) -> MediaOrm | None:
        async with Session_maker() as session:
            ret = await session.get(MediaOrm, value_id)
            return ret

    @classmethod
    async def update(cls, value_id: int, values: dict) -> int:
        async with Session_maker() as session:
            query = update(MediaOrm).where(MediaOrm.id == value_id).values(**values)
            ret = await session.execute(query)
            await session.commit()
            return ret.rowcount

