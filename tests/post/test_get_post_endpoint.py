"""Tests for 'get_post' endpoint."""

from __future__ import annotations


def test_get_post_returns_200_with_correct_response(
    client, db_with_one_account_one_post, token_for_testing, storage_with_one_image_and_preview,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("accounts/1/posts/1", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "account_id": 1,
        "description": "test",
        "file_id": 1,
        "preview_id": 2,
        "title": "test",
    }


def test_get_post_returns_404_with_correct_response(
    client, db_with_one_account_and_one_image, token_for_testing,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("accounts/1/posts/1", headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}
