"""Pydantic schemas for profile feature."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Profile(BaseModel):
    """Profile schema."""

    account_id: int

    avatar_id: int | None = Field(default=None, gt=0)
    background_id: int | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    info: str | None = Field(default=None, min_length=1, max_length=100, pattern=r"[A-Za-z.' \-()]+")
    username: str = Field(min_length=1, max_length=30, pattern=r"[a-z][a-z0-9_]")


class Profiles(BaseModel):
    """Profiles (plural) schema."""

    profiles: list[Profile]


class ProfileData(BaseModel):
    """Profile data schema."""

    avatar_id: int | None = Field(default=None, gt=0)
    background_id: int | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    info: str | None = Field(default=None, min_length=1, max_length=100, pattern=r"[A-Za-z.' \-()]+")
    username: str = Field(min_length=1, max_length=30, pattern=r"[a-z][a-z0-9_]")
