"""Image processor module."""
from __future__ import annotations

from pathlib import Path
from typing import Self, TYPE_CHECKING  # noqa: TCH003

from PIL import Image
from PIL.Image import Resampling
from PIL.ImageOps import contain

from src.shared.storage import Minio


if TYPE_CHECKING:
    from src.files.models import File


class ImageProcessor:  # pylint: disable=too-few-public-methods
    """Image processor class."""

    def __init__(self: Self, file: File, tmp_dir: Path) -> None:
        """Image processor constructor."""
        self._file = file

        self._file_path = Path(tmp_dir) / f"{file.filename}.{file.extension.value}"

        minio = Minio.get_client()
        minio.fget_object(
            bucket_name="files",
            object_name=str(file.id),
            file_path=self._file_path,
        )

    def create_preview(self: Self) -> Path:
        """Create preview of an image."""
        preview_path = self._file_path.parent / f"preview_{self._file.filename}.{self._file.extension.value}"
        with Image.open(self._file_path) as im:
            imr = contain(image=im, size=(700, 700), method=Resampling.BICUBIC)
            imr.save(preview_path, dpi=(300, 300))

        return preview_path
