"""Object storage utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

import minio

from src.config import config


if TYPE_CHECKING:
    from typing import Any, Final, Self

    from src.files.schemas import FileData


class Minio(minio.Minio):  # type: ignore[misc]
    """Minio subclass with custom functionality."""

    BUCKETS: Final = (
        "files",
    )

    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        """Initialize minio client."""
        super().__init__(*args, **kwargs)
        self._create_missing_buckets()

    def _create_missing_buckets(self: Self) -> None:  # pragma: no cover
        """Create Minio buckets which don't exist."""
        for bucket in self.BUCKETS:
            if not self.bucket_exists(bucket):
                self.make_bucket(bucket)

    @classmethod
    def get_client(cls: type[Minio]) -> Minio:
        """Get storage client."""
        return Minio(
            f"{config.MINIO_HOST}:{config.MINIO_PORT}",
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=False,
        )

    def upload_file(self: Self, file_id: int, file_data: FileData) -> None:
        """Upload file to storage."""
        self.put_object("files", str(file_id), file_data.data, file_data.size)

    def download_file(self: Self, file_id: int) -> bytes:
        """Return object data as HTTP response."""
        try:  # pylint: disable=too-many-try-statements
            response = self.get_object("files", str(file_id))
            file_data: bytes = response.data
        finally:
            response.close()
            response.release_conn()

        return file_data
