"""Controllers for following package endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from src.account.models import Account
from src.following.schemas import Followees, Followers, FollowingCounts
from src.following.schemas import Following as FollowingSchema


if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from src.auth.schemas import TokenPayload
    from src.following.schemas import NewFollowing


def create_following(db: Session, token: TokenPayload, new_following: NewFollowing) -> FollowingSchema:
    """Create a Following object."""
    if new_following.follower_id != token.account_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No rights to perform that action")

    account = Account.get(db, new_following.followee_id)
    if account.has_follower(db, new_following.follower_id):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Already following.")
    following = account.add_follower(db, new_following.follower_id)

    return FollowingSchema.model_validate(following, from_attributes=True)


def get_following_counts(db: Session, account_ids: list[int]) -> FollowingCounts:
    """Get following counts for account(s)."""
    counts = Account.get_counts(db=db, account_ids=account_ids)

    return FollowingCounts(following_counts=counts)


def get_followers(db: Session, account_id: int, limit: int, offset: int) -> Followers:
    """Get a list of an account's followers."""
    account = Account.get(db, account_id)
    followers = account.get_followers(db, limit, offset)

    return Followers(followers=followers)


def get_followees(db: Session, account_id: int, limit: int, offset: int) -> Followees:
    """Get a list of an account's followees."""
    account = Account.get(db, account_id)
    followees = account.get_followees(db, limit, offset)

    return Followees(followees=followees)


def remove_followee(db: Session, token: TokenPayload, account_id: int, followee_id: int) -> None:
    """Remove a followee."""
    if account_id != token.account_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No rights to perform that action.")

    account = Account.get(db, account_id)
    if not account.has_followee(db, followee_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No followee with that id.")

    account.remove_followee(db, followee_id)
