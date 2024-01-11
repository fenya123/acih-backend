"""Routes for feed package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.dependencies import get_token
from src.post.schemas import Posts


router = APIRouter(tags=["feed"])


@router.get(
    "/feed/accounts/{account_id}/posts/followed",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=Posts,
    status_code=status.HTTP_200_OK,
)
def get_followed_posts_feed(
    account_id: Annotated[int, Path()],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    limit: Annotated[int, Query()],  # noqa: ARG001
    offset: Annotated[int, Query()],  # noqa: ARG001
) -> None:
    """Get followed posts for an account."""


@router.get(
    "/feed/accounts/{account_id}/posts/suggested",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=Posts,
    status_code=status.HTTP_200_OK,
)
def get_suggested_posts_feed(
    account_id: Annotated[int, Path()],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    limit: Annotated[int, Query()],  # noqa: ARG001
    offset: Annotated[int, Query()],  # noqa: ARG001
) -> None:
    """Get suggested posts for an account."""
