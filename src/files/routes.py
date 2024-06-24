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
from src.shared.swagga import Description


router = APIRouter(tags=["files"])


@router.post(
    "/files",
    responses={
        status.HTTP_201_CREATED: {"description": "File uploaded, file info returned."},
        status.HTTP_401_UNAUTHORIZED: {"description": Description.HTTP_401},
        status.HTTP_403_FORBIDDEN: {"description": Description.HTTP_403},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {"description": "File exceeds size limit."},
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {"description": "Unsupported file extension."},
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
        status.HTTP_401_UNAUTHORIZED: {"description": Description.HTTP_401},
        status.HTTP_403_FORBIDDEN: {"description": Description.HTTP_403},
        status.HTTP_404_NOT_FOUND: {"description": Description.HTTP_404},
    },
    response_class=Response,
)
def download_file(
    db: Db,
    file_id: Annotated[int, Path(example=42)],
) -> Response:
    """Download file endpoint."""
    return controllers.download_file(db=db, file_id=file_id)
