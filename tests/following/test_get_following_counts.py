"""Tests for 'get_following_counts' endpoint."""

from __future__ import annotations


def test_get_following_counts_returns_200_with_correct_response(
    client, db_with_several_following_relationsips, token_for_testing,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("/following/counts?account_id=1&account_id=2&account_id=3", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "following_counts": [
            {"account_id": 1, "followers": 1, "followees": 2},
            {"account_id": 2, "followers": 2, "followees": 0},
            {"account_id": 3, "followers": 1, "followees": 2},
        ],
    }
