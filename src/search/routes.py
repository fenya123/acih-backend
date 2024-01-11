"""Routes for search package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.account.schemas import Accounts
from src.auth.dependencies import get_token


router = APIRouter(tags=["search"])


@router.get(
    "/search/accounts",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
    },
    response_model=Accounts,
    status_code=status.HTTP_200_OK,
)
def search_accounts(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    profile_username: Annotated[str, Query()],  # noqa: ARG001
    limit: Annotated[int, Query()],  # noqa: ARG001
    offset: Annotated[int, Query()],  # noqa: ARG001
) -> None:
    """Get accounts search result endpoint."""
