"""Routes for profile package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.dependencies import get_token
from src.auth.schemas import TokenPayload
from src.profile import controllers
from src.profile.schemas import Profile, ProfileData, Profiles
from src.shared.database import Db


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
    account_id: Annotated[int, Path()],
    token: Annotated[TokenPayload, Depends(get_token)],
    db: Db,
    profile_data: Annotated[ProfileData, Body()],
) -> Profile:
    """Update profile data endpoint."""
    return controllers.update_profile(account_id, db, profile_data, token)


@router.get(
    "/accounts/{account_id}/profile",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=Profile,
    status_code=status.HTTP_200_OK,
)
def get_profile(
    account_id: Annotated[int, Path()],
    db: Db,
    token: Annotated[TokenPayload, Depends(get_token)],  # noqa: ARG001
) -> Profile:
    """Get profile endpoint."""
    return controllers.get_profile(account_id, db)


@router.get(
    "/profiles",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
    },
    response_model=Profiles,
    status_code=status.HTTP_200_OK,
)
def get_profiles(
    account_ids: Annotated[list[int], Query(alias="account_id")],
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    db: Db,
) -> Profiles:
    """Get several profiles endpoint."""
    return controllers.get_profiles(account_ids, db)
