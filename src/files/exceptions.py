"""Files package exceptions."""

from __future__ import annotations

from fastapi import status

from src.shared.exceptions import EntityTooLargeException, NotFoundException, UnsupportedTypeException


class FileNotFoundException(NotFoundException):
    """File not found exception."""

    resource: str = "File"

    description = "Requested resource not found."
    detail = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND


class NoExtensionException(UnsupportedTypeException):
    """No extension exception."""

    description = "No file extension."
    detail = "File does not contain an extension."
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


class NoMimeTypeException(UnsupportedTypeException):
    """No mime type exception."""

    description = "No mime type specified."
    detail = "Request payload does not have a mime type specified."
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


class FileTooLargeException(EntityTooLargeException):
    """File too large exception."""

    description = "Request payload is too large."
    detail = "Request payload is too large, and cannot be handled."
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
