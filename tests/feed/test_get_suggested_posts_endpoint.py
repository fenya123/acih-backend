"""Tests for 'get_suggested_posts_feed' endpoint."""

from __future__ import annotations

import pytest


@pytest.mark.freeze_time("2024-06-09T14:31:36.577049Z")
def test_get_suggested_posts_feed_returns_200_with_correct_response(
    client, token_for_testing, db_with_three_accounts_several_posts_two_followings,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("/feed/posts/suggested?limit=10&offset=2", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "posts": [
            {
                "id": 7,
                "account_id": 2,
                "description": "test post 7",
                "file_id": 13,
                "preview_id": 14,
                "title": "test post 7",
                "created_at": "2024-06-09T14:32:36.577049Z",
            },
            {
                "id": 6,
                "account_id": 1,
                "description": "test post 6",
                "file_id": 11,
                "preview_id": 12,
                "title": "test post 6",
                "created_at": "2024-06-09T14:32:36.576049Z",
            },
           {
                "id": 5,
                "account_id": 2,
                "description": "test post 5",
                "file_id": 9,
                "preview_id": 10,
                "title": "test post 5",
                "created_at": "2024-06-09T14:32:36.575049Z",
            },
           {
                "id": 4,
                "account_id": 1,
                "description": "test post 4",
                "file_id": 7,
                "preview_id": 8,
                "title": "test post 4",
                "created_at": "2024-06-09T14:32:36.574049Z",
            },
           {
                "id": 1,
                "account_id": 1,
                "description": "test post 1",
                "file_id": 1,
                "preview_id": 2,
                "title": "test post 1",
                "created_at": "2024-06-09T14:32:36.571049Z",
            }],
    }
