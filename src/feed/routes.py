"""Routes for feed package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from src.auth.dependencies import get_token
from src.auth.schemas import TokenPayload
from src.feed import controllers
from src.post.schemas import Posts
from src.shared.database import Db


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
    db: Db,
    account_id: Annotated[int, Path()],
    token: Annotated[TokenPayload, Depends(get_token)],  # noqa: ARG001
    limit: Annotated[int, Query()],
    offset: Annotated[int, Query()],
) -> Posts:
    """Get followed posts for an account."""
    return controllers.get_followed_posts_feed(
        db=db,
        account_id=account_id,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/feed/posts/suggested",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
    },
    response_model=Posts,
    status_code=status.HTTP_200_OK,
)
def get_suggested_posts_feed(
    db: Db,
    token: Annotated[TokenPayload, Depends(get_token)],  # noqa: ARG001
    limit: Annotated[int, Query()],
    offset: Annotated[int, Query()],
) -> Posts:
    """Get suggested posts."""
    return controllers.get_suggested_posts_feed(
        db=db,
        limit=limit,
        offset=offset,
    )
