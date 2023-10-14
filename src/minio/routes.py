"""Routes for minio package."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from src.config import config
from src.shared.storage import Minio


router = APIRouter()


@router.post("/objects/{object_name}")
def add_object(
    object_name: str,
) -> dict[str, str]:
    """Add object to Minio bucket."""
    with tempfile.TemporaryDirectory() as tmp_dir:

        filepath: Path = Path(tmp_dir) / "foo.txt"  # pylint: disable = duplicate-code
        with filepath.open("wb") as f:
            f.write(b"Hello Minio!")

        client = Minio(
            f"{config.MINIO_HOST}:{config.MINIO_PORT}",
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=False,
        )
        client.fput_object("testbucket", object_name, filepath)
        objects = list(client.list_objects("testbucket"))

    return {
        "message": f"Object with key '{objects[0].object_name}' and size '{objects[0].size}' is created.",
    }


@router.get("/objects/")
def get_objects_list() -> dict[str, list[dict[str, Any]]]:
    """Get list of objects of a certain bucket."""
    client = Minio(
        f"{config.MINIO_HOST}:{config.MINIO_PORT}",
        access_key=config.MINIO_ACCESS_KEY,
        secret_key=config.MINIO_SECRET_KEY,
        secure=False,
    )

    objects = []
    for obj in list(client.list_objects("testbucket")):
        objects.append({
            "name": obj.object_name,
            "size": obj.size,
        })
    return {"objects": objects}
