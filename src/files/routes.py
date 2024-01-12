"""Routes for files package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status, UploadFile
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.dependencies import get_token
from src.files.schemas import File


router = APIRouter(tags=["files"])


@router.post(
    "/files",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {},
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {},
    },
    response_model=File,
    status_code=status.HTTP_201_CREATED,
)
def upload_file(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    file: UploadFile,  # noqa: ARG001
) -> None:
    """Upload file endpoint."""


@router.get(
    "/files/{file_id}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_class=FileResponse,
)
def download_file(
    file_id: Annotated[int, Path()],  # noqa: ARG001
) -> None:
    """Download file endpoint."""
