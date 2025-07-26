from datetime import datetime

from sqlalchemy import DateTime, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base
from src.media.enum.media_status import MediaStatus


class MediaOrm(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    s3_key: Mapped[str]
    status: Mapped[str] = mapped_column(SqlEnum(MediaStatus, name="status"))
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

