"""Controllers for files package endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Response, status

from src.files.models import File as FileModel
from src.files.schemas import File as FileSchema
from src.shared.storage import Minio


if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from src.files.schemas import FileData


def upload_file(
    db: Session,
    file_data: FileData,
) -> FileSchema:
    """Upload file."""
    client = Minio.get_client()
    file = FileModel.new_object(
        db=db,
        file_data=file_data,
    )
    client.upload_file(file.id, file_data)
    return FileSchema.model_validate(file, from_attributes=True)


def download_file(
    db: Session,
    file_id: int,
) -> Response:
    """Download file."""
    client = Minio.get_client()
    file = FileModel.get_file(db, file_id)
    data = client.download_file(file.id)
    return Response(status_code=status.HTTP_200_OK, content=data, media_type=file.mime_type.value)
