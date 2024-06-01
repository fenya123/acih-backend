"""Tests for 'create_post' endpoint."""

from __future__ import annotations

from pathlib import Path

from src.post.models import Post


def test_create_post_returns_201_with_correct_response(
    client, token_for_testing, db_with_one_account_and_one_image, storage_with_one_image,
):
    session = db_with_one_account_and_one_image
    body = {
        "description": "test desc",
        "file_id": 1,
        "title": "test title",
    }
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.post("/posts", json=body, headers=headers)

    assert response.status_code == 201
    post = session.query(Post).one()
    assert response.json() == {
        "id": 10000,
        "account_id": 1,
        "description": "test desc",
        "file_id": 1,
        "preview_id": 10000,
        "title": "test title",
        "created_at": post.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    }


def test_create_post_uploads_correct_preview_to_minio(
    client, token_for_testing, db_with_one_account_and_one_image, storage_with_one_image,
):
    minio = storage_with_one_image
    body = {
        "description": "test desc",
        "file_id": 1,
        "title": "test title",
    }
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.post("/posts", json=body, headers=headers)

    response = minio.get_object("files", "10000")
    assert response.data == (Path(__file__).parent / "image-preview.png").read_bytes()
