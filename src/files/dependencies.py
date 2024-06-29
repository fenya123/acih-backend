"""Dependencies module."""

from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import UploadFile  # noqa: TCH002
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.files.constants import MEGABYTE
from src.files.enums import Extension, MimeType
from src.files.exceptions import FileTooLargeException, NoExtensionException, NoMimeTypeException
from src.files.schemas import FileData


def get_new_file(file: UploadFile) -> FileData:
    """Validate uploaded file's data and return it as a new object."""
    filename = (file.filename or "")

    _, _, extension = filename.rpartition(".")
    if extension not in Extension.values():
        raise NoExtensionException

    mime_type = (file.content_type or "")
    if mime_type not in MimeType.values():
        raise NoMimeTypeException

    size = (file.size or 0)
    if size > 200 * MEGABYTE:  # pragma: no cover
        raise FileTooLargeException

    try:
        return FileData(
            extension=extension,
            filename=filename,
            mime_type=mime_type,
            size=size,
            data=file.file,
        )
    except ValidationError as e:
        raise RequestValidationError(errors=e.errors()) from e


def get_tmp_dir() -> Path:
    """Create temporary directory and return it's path."""
    return Path(tempfile.mkdtemp())
