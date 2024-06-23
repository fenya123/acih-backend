"""Pydantic schemas for profile feature."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class Profile(BaseModel):
    """Profile schema."""

    account_id: int

    avatar_id: int | None = Field(default=None, gt=0)
    background_id: int | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, min_length=1, max_length=1000,
                                    examples=["What a day to be able to read! 8-)"])
    info: str | None = Field(default=None, min_length=1, max_length=100, pattern=r"[A-Za-z.' \-()]+",
                             examples=["What does a book have in common with a crab?"])
    username: str = Field(min_length=1, max_length=30, pattern=r"[a-z][a-z0-9_]", examples=["bob1997"])
    created_at: datetime


class Profiles(BaseModel):
    """Profiles (plural) schema."""

    profiles: list[Profile]


class ProfileData(BaseModel):
    """Profile data schema."""

    avatar_id: int | None = Field(default=None, gt=0)
    background_id: int | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, min_length=1, max_length=1000,
                                    examples=["What a day to be able to read! 8-)"])
    info: str | None = Field(default=None, min_length=1, max_length=100, pattern=r"[A-Za-z.' \-()]+",
                             examples=["What a day to be able to read! 8-)"])
    username: str = Field(min_length=1, max_length=30, pattern=r"[a-z][a-z0-9_]")
