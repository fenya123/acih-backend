"""Tests for 'upload_file' endpoint."""

from __future__ import annotations

from datetime import datetime

import pytest

from src.files.enums import Extension, MimeType
from src.files.models import File


def test_upload_file_creates_db_entry(client, db_empty):
    session = db_empty
    files = {"file": ("testjpeg.jpg", b"some file data in bytes", "image/jpeg")}
    headers = {"Authorization": "Bearer token-placeholder"}

    response = client.post("/files", files=files, headers=headers)

    assert response.status_code == 201
    files = session.query(File).where(File.filename == "testjpeg.jpg").all()
    assert len(files) == 1
    assert files[0].id == 10000
    assert files[0].extension == Extension.JPG
    assert files[0].filename == "testjpeg.jpg"
    assert files[0].mime_type == MimeType.IMAGE_JPEG
    assert files[0].size == 23
    assert isinstance(files[0].upload_ts, datetime)


def test_upload_file_returns_201_with_correct_response(client, db_empty):
    session = db_empty
    files = {"file": ("testjpeg.jpg", b"some file data in bytes", "image/jpeg")}
    headers = {"Authorization": "Bearer token-placeholder"}

    response = client.post("/files", files=files, headers=headers)

    assert response.status_code == 201
    uploaded_file = session.query(File).where(File.filename == "testjpeg.jpg").one()
    assert response.json() == {
        "extension": "jpg",
        "filename": "testjpeg.jpg",
        "id": 10000,
        "mime_type": "image/jpeg",
        "size": 23,
        "upload_ts": uploaded_file.upload_ts.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    }


def test_upload_file_adds_correct_object_to_storage(client, storage_empty):
    minio = storage_empty
    files = {"file": ("testjpeg.jpg", b"some file data in bytes", "image/jpeg")}
    headers = {"Authorization": "Bearer token-placeholder"}

    response = client.post("/files", files=files, headers=headers)

    assert response.status_code == 201
    objects = list(minio.list_objects("files"))
    assert len(objects) == 1
    assert objects[0].object_name == "10000"
    assert objects[0].size == 23
    assert minio.get_object("files", "10000").read() == b"some file data in bytes"


def test_upload_file_with_file_without_filename_returns_422_with_correct_response(client):
    files = {"file": (".png", b"some file data in bytes", "image/jpeg")}
    headers = {"Authorization": "Bearer token-placeholder"}

    response = client.post("/files", files=files, headers=headers)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error",
                "loc": ["filename"],
                "msg": "Value error, File does not have a name.",
                "input": ".png",
                "ctx": {"error": {}},
                "url": "https://errors.pydantic.dev/2.5/v/value_error",
            },
        ],
    }


def test_upload_file_without_extension_returns_415_with_correct_response(client):
    files = {"file": ("testjpeg", b"some file data in bytes", "image/jpeg")}
    headers = {"Authorization": "Bearer token-placeholder"}

    response = client.post("/files", files=files, headers=headers)

    assert response.status_code == 415
    assert response.json() == {"detail": "File does not contain an extension."}


def test_upload_file_without_mime_type_returns_415_with_correct_response(client):
    files = {"file": ("testjpeg.jpg", b"some file data in bytes", "")}
    headers = {"Authorization": "Bearer token-placeholder"}

    response = client.post("/files", files=files, headers=headers)

    assert response.status_code == 415
    assert response.json() == {"detail": "Mime type is not defined."}


@pytest.mark.skip(reason="We haven't found a way to reproduce large file in test without having 200mb loaded in memory")
def test_upload_file_with_incorrect_size_returns_413_with_correct_response(client):
    files = {"file": ("testjpeg.jpg", b"some file data in bytes", "image/jpeg")}
    headers = {"Authorization": "Bearer token-placeholder"}

    response = client.post("/files", files=files, headers=headers)

    assert response.status_code == 413
