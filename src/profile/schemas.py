"""Pydantic schemas for profile feature."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Profile(BaseModel):
    """Profile schema."""

    account_id: int

    avatar_id: str | None = None
    background_id: str | None = None
    description: str | None = Field(min_length=1, max_length=1000)
    info: str | None = Field(min_length=1, max_length=100, pattern=r"[\w.` \-()]+")
    username: str = Field(min_length=1, max_length=30, pattern=r"[a-z][a-z0-9_]")


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
