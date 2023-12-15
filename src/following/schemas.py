"""Pydantic schemas for following feature."""

from __future__ import annotations

from pydantic import BaseModel


class NewFollowing(BaseModel):
    """Schema for a following to be created."""

    follower_id: int
    followee_id: int


class Following(BaseModel):
    """Following schema."""

    id: int  # noqa: A003

    followee_id: int
    follower_id: int


class Follower(BaseModel):
    """Follower schema."""

    account_id: int


class Followee(BaseModel):
    """Followee schema."""

    account_id: int


class Followers(BaseModel):
    """Followers schema."""

    followers: list[Follower]


class Followees(BaseModel):
    """Followees schema."""

    followees: list[Followee]


class FollowingCount(BaseModel):
    """Following count schema."""

    account_id: int
    followers: int
    followees: int


class FollowingCounts(BaseModel):
    """Following counts (plural) schema."""

    following_counts: list[FollowingCount]
