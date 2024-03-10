"""Tests for 'get_followers' endpoint."""

from __future__ import annotations


def test_get_followers_returns_200_with_correct_response(
    client, token_for_testing, db_with_several_following_relationsips,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("/accounts/2/followers?limit=1&offset=1", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"followers": [{"account_id": 3}]}
