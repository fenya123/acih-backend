"""Pydantic schemas for profile feature."""

from __future__ import annotations

from pydantic import BaseModel


class Profile(BaseModel):
    """Profile schema."""

    account_id: int

    avatar_id: str | None = None
    background_id: str | None = None
    description: str | None = None
    info: str | None = None
    username: str


class Profiles(BaseModel):
    """Profiles (plural) schema."""

    profiles: list[Profile]


class ProfileData(BaseModel):
    """Profile data schema."""

    avatar_id: str | None = None
    background_id: str | None = None
    description: str | None = None
    info: str | None = None
    username: str
