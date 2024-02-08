"""Routes for auth package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from fastapi.security import HTTPAuthorizationCredentials

from src.auth import controllers
from src.auth.dependencies import get_token
from src.auth.schemas import Credentials, SessionWithToken
from src.shared.database import Db


router = APIRouter(tags=["auth"])


@router.post(
    "/sessions",
    responses={
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=SessionWithToken,
    status_code=status.HTTP_201_CREATED,
)
def create_session(credentials: Annotated[Credentials, Body()], db: Db) -> SessionWithToken:
    """Create session endpoint."""
    return controllers.create_session(credentials, db)


@router.delete(
    "/accounts/{account_id}/sessions/{session_id}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_session(
    account_id: Annotated[int, Path()],  # noqa: ARG001
    session_id: Annotated[int, Path()],  # noqa: ARG001
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
) -> None:
    """Remove session endpoint."""
