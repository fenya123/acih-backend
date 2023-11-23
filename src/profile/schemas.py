"""Pydantic schemas for profile feature."""

from __future__ import annotations

from pydantic import BaseModel


class Profile(BaseModel):
    """Profile schema."""

    account_id: int

    avatar_id: str | None
    background_id: str | None
    description: str | None
    info: str | None
    username: str
