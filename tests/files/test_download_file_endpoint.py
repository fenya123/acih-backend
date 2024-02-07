"""Tests for 'download_file' endpoint."""

from __future__ import annotations


def test_download_file_returns_200_with_correct_response(client, storage_with_one_object, db_with_one_file):
    response = client.get("/files/10000")

    assert response.status_code == 200
    assert response.content == b"Mockbytesobject"
    assert response.headers["content-type"] == "image/jpeg"
    assert response.headers["content-length"] == "15"


def test_download_file_with_nonexistent_file_returns_404_with_correct_message(client, db_empty, storage_empty):
    response = client.get("/files/1337")

    assert response.status_code == 404
    assert response.json() == {"detail": "Requested file not found."}
