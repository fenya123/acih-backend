"""Routes for files package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import Response
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.dependencies import get_token
from src.files import controllers
from src.files.dependencies import get_new_file
from src.files.schemas import File, FileData
from src.shared.database import Db


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
    db: Db,
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(get_token)],  # noqa: ARG001
    file_data: Annotated[FileData, Depends(get_new_file)],
) -> File:
    """Upload file endpoint."""
    return controllers.upload_file(db=db, file_data=file_data)


@router.get(
    "/files/{file_id}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_403_FORBIDDEN: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    response_class=Response,
)
def download_file(
    db: Db,
    file_id: Annotated[int, Path()],
) -> Response:
    """Download file endpoint."""
    return controllers.download_file(db=db, file_id=file_id)
