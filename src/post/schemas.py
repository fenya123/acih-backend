"""Pydantic schemas for post feature."""

from __future__ import annotations

from pydantic import BaseModel


class Post(BaseModel):
    """Post schema."""

    id: int  # noqa: A003

    account_id: int
    description: str | None
    file_id: str
    preview_id: str
    title: str | None


class Posts(BaseModel):
    """Posts (plural) schema."""

    posts: list[Post]


class PostContent(BaseModel):
    """Post content schema."""

    description: str | None
    file_id: str
    preview_id: str
    title: str | None


class PostsCount(BaseModel):
    """Posts count schema."""

    account_id: int
    count: int


class PostsCounts(BaseModel):
    """Post counts (plural) schema."""

    posts_counts: list[PostsCount]
