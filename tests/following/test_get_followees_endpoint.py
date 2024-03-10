"""Tests for 'get_followees' endpoint."""

from __future__ import annotations


def test_get_followees_returns_200_with_correct_response(
    client, token_for_testing, db_with_several_following_relationsips,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("/accounts/3/followees?limit=1&offset=1", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"followees": [{"account_id": 2}]}
