"""Tests for 'get_profiles' endpoint."""

from __future__ import annotations


def test_get_profiles_returns_200_with_correct_response(client, db_with_two_accounts_one_session, token_for_testing):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("/profiles?account_id=1&account_id=2&account_id=3", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "profiles": [
            {
                "account_id": 1,
                "avatar_id": None,
                "background_id": None,
                "description": None,
                "info": None,
                "username": "test",
            },
            {
                "account_id": 2,
                "avatar_id": None,
                "background_id": None,
                "description": None,
                "info": None,
                "username": "test02",
            },
        ],
    }
