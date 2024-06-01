"""Tests for 'get_posts_counts' endpoint."""

from __future__ import annotations


def test_get_following_counts_returns_200_with_correct_response(
    client, db_with_two_accounts_several_posts, token_for_testing,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("/posts/counts?account_id=1&account_id=2", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "posts_counts": [
            {
                "account_id": 2,
                "count": 1,
            },
            {
                "account_id": 1,
                "count": 2,
            },
        ],
    }
