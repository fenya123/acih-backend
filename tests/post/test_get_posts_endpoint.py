"""Tests for 'get_posts' endpoint."""

from __future__ import annotations

from src.post.models import Post


def test_get_posts_returns_200_with_correct_response(
    client, db_with_one_account_one_post, token_for_testing, storage_with_one_image_and_preview,
):
    session = db_with_one_account_one_post
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("/accounts/1/posts?limit=1&offset=0", headers=headers)

    assert response.status_code == 200
    post = session.query(Post).one()
    assert response.json() == {
        "posts": [
            {
                "account_id": 1,
                "description": "test",
                "file_id": 1,
                "id": 1,
                "preview_id": 2,
                "title": "test",
                "created_at": post.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            },
        ],
    }
