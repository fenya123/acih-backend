"""Routes for post package."""


from __future__ import annotations

import pathlib
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Path, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.dependencies import get_token
from src.auth.schemas import TokenPayload
from src.files.dependencies import get_tmp_dir
from src.post import controllers
from src.post.schemas import Post, PostContent, Posts, PostsCounts
from src.shared.database import Db


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
    db: Db,
    background_tasks: BackgroundTasks,
    token: Annotated[TokenPayload, Depends(get_token)],
    tmp_dir: Annotated[pathlib.Path, Depends(get_tmp_dir)],
    post_content: Annotated[PostContent, Body()],
) -> Post:
    """Create post."""
    return controllers.create_post(
        db=db,
        token=token,
        post_content=post_content,
        background_tasks=background_tasks,
        tmp_dir=tmp_dir,
    )


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
    db: Db,
    account_id: Annotated[int, Path()],
    token: Annotated[TokenPayload, Depends(get_token)],  # noqa: ARG001
    post_id: Annotated[int, Path()],
) -> Post:
    """Get an account's post."""
    return controllers.get_post(
        db=db,
        account_id=account_id,
        post_id=post_id,
    )


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
    db: Db,
    account_id: Annotated[int, Path()],
    token: Annotated[TokenPayload, Depends(get_token)],  # noqa: ARG001
    limit: Annotated[int, Query()],
    offset: Annotated[int, Query()],
) -> Posts:
    """Get a list of an account's posts."""
    return controllers.get_posts(
        db=db,
        account_id=account_id,
        limit=limit,
        offset=offset,
    )


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
