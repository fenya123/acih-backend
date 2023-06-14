"""Contains placeholder tests needed to check whether tests functions correctly or not."""
from __future__ import annotations


def func(number: int) -> int:
    """Use this function as a placeholder for test."""
    return number + 1


def func1(number: int) -> int:  # pragma: no cover
    """Use this function as a placeholder for test."""
    if number is True:
        return number - 1
    return number
