"""Pydantic schemas for following feature."""

from __future__ import annotations

from pydantic import BaseModel, model_validator


class NewFollowing(BaseModel):
    """Schema for a following to be created."""

    follower_id: int
    followee_id: int

    @model_validator(mode="after")
    def check_following_self(self) -> NewFollowing:  # noqa: ANN101
        """Check if passed ids are the same (trying to follow self)."""
        if self.follower_id == self.followee_id:
            msg = "Can't follow self."
            raise ValueError(msg)
        return self


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
