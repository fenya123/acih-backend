"""Pydantic schemas for files feature."""

from __future__ import annotations

from datetime import datetime
from tempfile import SpooledTemporaryFile

from pydantic import BaseModel, Field, field_validator

from src.files.constants import BYTE, MEGABYTE
from src.files.enums import Extension, MimeType


class File(BaseModel):
    """Schema for a file ORM model."""

    id: int  # noqa: A003

    extension: Extension
    filename: str
    mime_type: MimeType
    size: int = Field(gt=1 * BYTE, le=200 * MEGABYTE)
    upload_ts: datetime


class FileData(BaseModel, arbitrary_types_allowed=True):
    """Schema for a file's data."""

    extension: Extension
    filename: str
    mime_type: MimeType
    size: int = Field(gt=1 * BYTE, le=200 * MEGABYTE)
    data: SpooledTemporaryFile[bytes]

    @field_validator("filename")
    @classmethod
    def _validate_filename(cls: type[FileData], value: str) -> str:
        filename, _, _ = value.rpartition(".")
        if not filename:
            msg = "File does not have a name."
            raise ValueError(msg)
        return value
