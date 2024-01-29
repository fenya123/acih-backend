"""Package for files models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, Session

from src.files.enums import Extension, MimeType
from src.files.schemas import FileData
from src.shared.database import Base
from src.shared.datetime import utcnow


class File(Base):  # pylint: disable=too-few-public-methods
    """ORM model for the 'file' table."""

    __tablename__ = "file"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)  # noqa: A003

    extension: Mapped[Extension] = mapped_column(Enum(Extension, name="extension_enum"), nullable=False)
    filename: Mapped[str] = mapped_column(String(), nullable=False)
    mime_type: Mapped[MimeType] = mapped_column(Enum(MimeType, name="mimetype_enum"), nullable=False)
    size: Mapped[int] = mapped_column(Integer(), nullable=False)
    upload_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    @classmethod
    def new_object(
        cls: type[File],
        db: Session,
        file_data: FileData,
    ) -> File:
        """Create a new file object."""
        file = File(
            extension=file_data.extension,
            filename=file_data.filename,
            mime_type=file_data.mime_type,
            size=file_data.size,
        )
        db.add(file)
        db.flush()
        return file
