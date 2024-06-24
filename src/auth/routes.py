"""Routes for auth package."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, status

from src.auth import controllers
from src.auth.dependencies import get_token
from src.auth.schemas import Credentials, SessionWithToken, TokenPayload
from src.shared.database import Db
from src.shared.swagga import Description


router = APIRouter(tags=["auth"])


@router.post(
    "/sessions",
    responses={
        status.HTTP_201_CREATED: {"description": "Sign In - session object is created along with bearer token."},
        status.HTTP_404_NOT_FOUND: {"description": Description.HTTP_404},
    },
    response_model=SessionWithToken,
    status_code=status.HTTP_201_CREATED,
)
def create_session(credentials: Annotated[Credentials, Body()], db: Db) -> SessionWithToken:
    """Create session object along with JWT token."""
    return controllers.create_session(credentials, db)


@router.delete(
    "/accounts/{account_id}/sessions/{session_id}",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Sign Out - session object is removed."},
        status.HTTP_401_UNAUTHORIZED: {"description": Description.HTTP_401},
        status.HTTP_403_FORBIDDEN: {"description": Description.HTTP_403},
        status.HTTP_404_NOT_FOUND: {"description": Description.HTTP_404},
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_session(
    account_id: Annotated[int, Path(example=42)],
    session_id: Annotated[UUID, Path(example=42)],
    token: Annotated[TokenPayload, Depends(get_token)],
    db: Db,
) -> None:
    """Remove session database object invalidating any tokens associated with it."""
    return controllers.remove_session(account_id, token, db, session_id)
