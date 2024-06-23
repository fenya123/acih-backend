"""Routes for following package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status

from src.auth.dependencies import get_token
from src.auth.schemas import TokenPayload
from src.following import controllers
from src.following.schemas import Followees, Followers, Following, FollowingCounts, NewFollowing
from src.shared.database import Db
from src.shared.swagger import responses


router = APIRouter(tags=["following"])


@router.post(
    "/followings",
    responses={
        status.HTTP_201_CREATED: {"description": "Following object's info is returned."},
        status.HTTP_401_UNAUTHORIZED: responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=Following,
    status_code=status.HTTP_201_CREATED,
)
def create_following(
    db: Db,
    token: Annotated[TokenPayload, Depends(get_token)],
    new_following: Annotated[NewFollowing, Body()],
) -> Following:
    """Create a Following object."""
    return controllers.create_following(db, token, new_following)


@router.get(
    "/following/counts",
    responses={
        status.HTTP_200_OK: {"description": "Returns number of followers/followees for each account."},
        status.HTTP_401_UNAUTHORIZED: responses[status.HTTP_401_UNAUTHORIZED],
    },
    response_model=FollowingCounts,
    status_code=status.HTTP_200_OK,
)
def get_following_counts(
    account_ids: Annotated[list[int], Query(alias="account_id", example=[42, 24])],
    db: Db,
    token: Annotated[TokenPayload, Depends(get_token)],  # noqa: ARG001
) -> FollowingCounts:
    """Get following counts for account(s)."""
    return controllers.get_following_counts(db, account_ids)


@router.get(
    "/accounts/{account_id}/followers",
    responses={
        status.HTTP_200_OK: {"description": "Returns list of accounts that follow an account."},
        status.HTTP_401_UNAUTHORIZED: responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_404_NOT_FOUND: responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=Followers,
    status_code=status.HTTP_200_OK,
)
def get_followers(
    account_id: Annotated[int, Path(example=42)],
    db: Db,
    token: Annotated[TokenPayload, Depends(get_token)],  # noqa: ARG001
    limit: Annotated[int, Query(example=5)],
    offset: Annotated[int, Query(example=5)],
) -> Followers:
    """Get a list of an account's followers."""
    return controllers.get_followers(db, account_id, limit, offset)


@router.get(
    "/accounts/{account_id}/followees",
    responses={
        status.HTTP_200_OK: {"description": "Returns a list of accounts that an account follows."},
        status.HTTP_401_UNAUTHORIZED: responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_404_NOT_FOUND: responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=Followees,
    status_code=status.HTTP_200_OK,
)
def get_followees(
    account_id: Annotated[int, Path(example=42)],
    db: Db,
    token: Annotated[TokenPayload, Depends(get_token)],  # noqa: ARG001
    limit: Annotated[int, Query(example=5)],
    offset: Annotated[int, Query(example=5)],
) -> Followees:
    """Get a list of an account's followees."""
    return controllers.get_followees(db, account_id, limit, offset)


@router.delete(
    "/accounts/{account_id}/followees/{followee_id}",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Following relationship is removed."},
        status.HTTP_401_UNAUTHORIZED: responses[status.HTTP_401_UNAUTHORIZED],
        status.HTTP_403_FORBIDDEN: responses[status.HTTP_403_FORBIDDEN],
        status.HTTP_404_NOT_FOUND: responses[status.HTTP_404_NOT_FOUND],
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_followee(
    account_id: Annotated[int, Path(example=42)],
    db: Db,
    token: Annotated[TokenPayload, Depends(get_token)],
    followee_id: Annotated[int, Path(example=42)],
) -> None:
    """Remove a followee."""
    return controllers.remove_followee(db, token, account_id, followee_id)
