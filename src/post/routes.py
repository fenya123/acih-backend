"""Routes for post package."""


from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.dependencies import get_token
from src.post.schemas import Post, PostContent, Posts, PostsCounts


router = APIRouter(tags=["post"])


@router.post(
    "/posts",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
    },
    response_model=Post,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    post_content: Annotated[PostContent, Body()],  # noqa: ARG001
) -> None:
    """Create post."""


@router.get(
    "/accounts/{account_id}/posts/{post_id}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=Post,
    status_code=status.HTTP_200_OK,
)
def get_post(
    account_id: Annotated[int, Path()],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    post_id: Annotated[int, Path()],  # noqa: ARG001
) -> None:
    """Get an account's post."""


@router.get(
    "/accounts/{account_id}/posts",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=Posts,
    status_code=status.HTTP_200_OK,
)
def get_posts(
    account_id: Annotated[int, Path()],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Get a list of an account's posts."""


@router.get(
    "/posts/counts",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
    },
    response_model=PostsCounts,
    status_code=status.HTTP_200_OK,
)
def get_posts_counts(
    account_ids: Annotated[list[int], Query(alias="account_id")],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Get several profiles endpoint."""
