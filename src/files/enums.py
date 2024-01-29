"""Enumerations of file package."""

from __future__ import annotations

from src.shared.enums import Enum


class MimeType(Enum):
    """Mime type enumeration."""

    IMAGE_PNG = "image/png"
    IMAGE_JPEG = "image/jpeg"


class Extension(Enum):
    """Extension enumeration."""

    JPE = "jpe"
    JPEG = "jpeg"
    JPG = "jpg"
    PNG = "png"
