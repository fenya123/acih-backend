"""Pydantic schemas for files feature."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from src.files.enums import Extension, MimeType


class File(BaseModel):
    """Schema for a file's data."""

    id: int  # noqa: A003

    extension: Extension
    filename: str
    mime_type: MimeType
    size: int
    upload_ts: datetime
