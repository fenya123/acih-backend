"""Object storage utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

import minio

from src.config import config


if TYPE_CHECKING:
    from typing import Any, Final, Self


class Minio(minio.Minio):  # type: ignore[misc]
    """Minio subclass with custom functionality."""

    BUCKETS: Final = (
        "testbucket",
    )

    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        """Initialize minio client."""
        super().__init__(*args, **kwargs)
        self._create_missing_buckets()

    def _create_missing_buckets(self: Self) -> None:
        """Create Minio buckets which don't exist."""
        for bucket in self.BUCKETS:
            if not self.bucket_exists(bucket):
                self.make_bucket(bucket)


if __name__ == "__main__":
    # pylint: disable=duplicate-code
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp_dir:

        filepath = Path(tmp_dir) / "testobject.txt"
        with filepath.open("wb") as f:
            f.write(b"Hello Minio!")

        client = Minio(
            f"{config.MINIO_HOST}:{config.MINIO_PORT}",
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=False,
        )
        client.fput_object("testbucket", "testobject", filepath)

        objects = list(client.list_objects("testbucket"))
        print(f"Object with key '{objects[0].object_name}' and size '{objects[0].size}' is created.")  # noqa: T201
        print(f"Total objects in 'testbucket': {len(objects)}")  # noqa: T201
    # pylint: enable=duplicate-code
