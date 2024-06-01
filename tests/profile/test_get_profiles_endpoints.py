"""Tests for 'get_profiles' endpoint."""

from __future__ import annotations

from src.profile.models import Profile


def test_get_profiles_returns_200_with_correct_response(client, db_with_two_accounts_one_session, token_for_testing):
    session = db_with_two_accounts_one_session
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("/profiles?account_id=1&account_id=2&account_id=3", headers=headers)

    assert response.status_code == 200
    profiles = session.query(Profile).order_by(Profile.account_id).all()
    assert response.json() == {
        "profiles": [
            {
                "account_id": 1,
                "avatar_id": None,
                "background_id": None,
                "description": None,
                "info": None,
                "username": "test",
                "created_at": profiles[0].created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            },
            {
                "account_id": 2,
                "avatar_id": None,
                "background_id": None,
                "description": None,
                "info": None,
                "username": "test02",
                "created_at": profiles[1].created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            },
        ],
    }
