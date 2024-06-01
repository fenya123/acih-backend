"""Tests for 'get_profile' endpoint."""

from __future__ import annotations

from src.profile.models import Profile


def test_get_profile_returns_200_witch_correct_response(client, db_with_one_account_one_session, token_for_testing):
    session = db_with_one_account_one_session
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("/accounts/1/profile", headers=headers)

    assert response.status_code == 200
    profile = session.query(Profile).one()
    assert response.json() == {
        "account_id": 1,
        "avatar_id": None,
        "background_id": None,
        "description": None,
        "info": None,
        "username": "test",
        "created_at": profile.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    }
