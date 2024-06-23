"""Pydantic schemas for post feature."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class Post(BaseModel):
    """Post schema."""

    id: int  # noqa: A003

    account_id: int
    description: str | None = Field(default=None, min_length=1, max_length=1000,
                                    examples=["What a day to be able to read! 8-)"])
    file_id: int
    preview_id: int
    title: str | None = Field(default=None, min_length=1, max_length=100,
                              examples=["What does a book have in common with a crab?"])
    created_at: datetime


class Posts(BaseModel):
    """Posts (plural) schema."""

    posts: list[Post]


class PostContent(BaseModel):
    """Post content schema."""

    description: str | None = Field(default=None, min_length=1, max_length=1000,
                                    examples=["What a day to be able to read! 8-)"])
    file_id: int
    title: str | None = Field(default=None, min_length=1, max_length=100,
                              examples=["What does a book have in common with a crab?"])


class PostsCount(BaseModel):
    """Posts count schema."""

    account_id: int
    count: int


class PostsCounts(BaseModel):
    """Post counts (plural) schema."""

    posts_counts: list[PostsCount]
