from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class FileOrm(Base):
    __tablename__ = "file"

    id: Mapped[int] = mapped_column(primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey("media.id"))
    file_name: Mapped[str]
    s3_key: Mapped[str]
    content_type: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime)

