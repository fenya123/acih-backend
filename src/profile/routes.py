"""Routes for profile package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.dependencies import get_token
from src.profile.schemas import Profile, ProfileData, Profiles


router = APIRouter(tags=["profile"])


@router.put(
    "/accounts/{account_id}/profile",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=Profile,
    status_code=status.HTTP_200_OK,
)
def update_profile(
    account_id: Annotated[int, Path()],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    profile_data: Annotated[ProfileData, Body()],  # noqa: ARG001
) -> None:
    """Update profile data endpoint."""


@router.get(
    "/accounts/{account_id}/profile",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=Profile,
    status_code=status.HTTP_200_OK,
)
def get_profile(
    account_id: Annotated[int, Path()],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Get profile endpoint."""


@router.get(
    "/profiles",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
    },
    response_model=Profiles,
    status_code=status.HTTP_200_OK,
)
def get_profiles(
    account_ids: Annotated[list[int], Query(alias="account_id")],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Get several profiles endpoint."""
