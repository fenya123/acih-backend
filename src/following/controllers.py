"""Controllers for following package endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from src.account.models import Account
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
