"""Module for exception utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Self


class NotFoundException(Exception):
    """Raised when some entity hasn't been found."""

    def __init__(self: Self, detail: str) -> None:
        """Initialize object."""
        self.detail = detail
