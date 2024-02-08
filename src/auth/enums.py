"""Enumerations for authorization package."""

from __future__ import annotations

from enum import Enum


class Algorithm(Enum):
    """JWT algorithms."""

    HS256 = "HS256"
