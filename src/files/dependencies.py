"""Dependencies module."""

from __future__ import annotations

from fastapi import HTTPException, status, UploadFile  # noqa: TCH002
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.files.constants import MEGABYTE
from src.files.enums import Extension, MimeType
from src.files.schemas import FileData


def get_new_file(file: UploadFile) -> FileData:
    """Validate uploaded file's data and return it as a new object."""
    filename = (file.filename or "")

    _, _, extension = filename.rpartition(".")
    if extension not in Extension.values():
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File does not contain an extension.",
        )

    mime_type = (file.content_type or "")
    if mime_type not in MimeType.values():
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Mime type is not defined.",
        )

    size = (file.size or 0)
    if size > 200 * MEGABYTE:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size is too large.",
        )

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
