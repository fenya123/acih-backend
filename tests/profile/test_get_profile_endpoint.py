"""Tests for 'get_profile' endpoint."""

from __future__ import annotations


def test_get_profile_returns_200_witch_correct_response(client, db_with_one_account_one_session, token_for_testing):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("/accounts/1/profile", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "account_id": 1,
        "avatar_id": None,
        "background_id": None,
        "description": None,
        "info": None,
        "username": "test",
    }
