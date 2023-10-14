"""Object storage utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING

import minio


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

    def _create_missing_buckets(self: Self) -> None:  # pragma: no cover
        """Create Minio buckets which don't exist."""
        for bucket in self.BUCKETS:
            if not self.bucket_exists(bucket):
                self.make_bucket(bucket)
