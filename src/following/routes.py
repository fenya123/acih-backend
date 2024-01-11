"""Routes for following package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.dependencies import get_token
from src.following.schemas import Followees, Followers, Following, FollowingCounts, NewFollowing


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
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    new_following: Annotated[NewFollowing, Body()],  # noqa: ARG001
) -> None:
    """Create a Following object."""


@router.get(
    "/following/counts",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
    },
    response_model=FollowingCounts,
    status_code=status.HTTP_200_OK,
)
def get_following_counts(
    account_ids: Annotated[list[int], Query(alias="account_id")],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Get following counts for account(s)."""


@router.get(
    "/accounts/{accounts_id}/followers",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=Followers,
    status_code=status.HTTP_200_OK,
)
def get_followers(
    account_id: Annotated[int, Path()],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    limit: Annotated[int, Query()],  # noqa: ARG001
    offset: Annotated[int, Query()],  # noqa: ARG001
) -> None:
    """Get a list of an account's followers."""


@router.get(
    "/accounts/{account_id}/followees",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=Followees,
    status_code=status.HTTP_200_OK,
)
def get_followees(
    account_id: Annotated[int, Path()],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    limit: Annotated[int, Query()],  # noqa: ARG001
    offset: Annotated[int, Query()],  # noqa: ARG001
) -> None:
    """Get a list of an account's followees."""


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
    account_id: Annotated[int, Path()],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    followee_id: Annotated[int, Path()],  # noqa: ARG001
) -> None:
    """Remove a followee."""
