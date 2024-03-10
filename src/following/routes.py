"""Routes for following package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status

from src.auth.dependencies import get_token
from src.auth.schemas import TokenPayload
from src.following import controllers
from src.following.schemas import Followees, Followers, Following, FollowingCounts, NewFollowing
from src.shared.database import Db


router = APIRouter(tags=["following"])


@router.post(
    "/followings",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
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
        status.HTTP_401_UNAUTHORIZED: {},
    },
    response_model=FollowingCounts,
    status_code=status.HTTP_200_OK,
)
def get_following_counts(
    account_ids: Annotated[list[int], Query(alias="account_id")],
    db: Db,
    token: Annotated[TokenPayload, Depends(get_token)],  # noqa: ARG001
) -> FollowingCounts:
    """Get following counts for account(s)."""
    return controllers.get_following_counts(db, account_ids)


@router.get(
    "/accounts/{account_id}/followers",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=Followers,
    status_code=status.HTTP_200_OK,
)
def get_followers(
    account_id: Annotated[int, Path()],
    db: Db,
    token: Annotated[TokenPayload, Depends(get_token)],  # noqa: ARG001
    limit: Annotated[int, Query()],
    offset: Annotated[int, Query()],
) -> Followers:
    """Get a list of an account's followers."""
    return controllers.get_followers(db, account_id, limit, offset)


@router.get(
    "/accounts/{account_id}/followees",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=Followees,
    status_code=status.HTTP_200_OK,
)
def get_followees(
    account_id: Annotated[int, Path()],
    db: Db,
    token: Annotated[TokenPayload, Depends(get_token)],  # noqa: ARG001
    limit: Annotated[int, Query()],
    offset: Annotated[int, Query()],
) -> Followees:
    """Get a list of an account's followees."""
    return controllers.get_followees(db, account_id, limit, offset)


@router.delete(
    "/accounts/{account_id}/followees/{followee_id}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_followee(
    account_id: Annotated[int, Path()],
    db: Db,
    token: Annotated[TokenPayload, Depends(get_token)],
    followee_id: Annotated[int, Path()],
) -> None:
    """Remove a followee."""
    return controllers.remove_followee(db, token, account_id, followee_id)
