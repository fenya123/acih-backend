"""Module for enum utilities."""

from __future__ import annotations

import enum


class Enum(enum.Enum):
    """Base enum class customized for project needs."""

    @classmethod
    def values(cls: type[Enum]) -> tuple[str, ...]:
        """Get enum values."""
        return tuple(e.value for e in tuple(cls))
