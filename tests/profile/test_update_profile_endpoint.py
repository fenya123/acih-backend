"""Tests for 'update_profile' endpoint."""

from __future__ import annotations

from sqlalchemy import select

from src.account.models import Account


def test_update_profile_returns_200_with_correct_response(client, db_with_one_account_and_two_files, token_for_testing):
    json = {
        "avatar_id": 1,
        "background_id": 2,
        "description": "test",
        "info": "test",
        "username": "test_test",
    }
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.put("/accounts/1/profile", json=json, headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "account_id": 1,
        "avatar_id": 1,
        "background_id": 2,
        "description": "test",
        "info": "test",
        "username": "test_test",
    }


def test_update_profile_updates_associated_db_entity(client, db_with_one_account_and_two_files, token_for_testing):
    session = db_with_one_account_and_two_files
    json = {
        "avatar_id": 1,
        "background_id": 1,
        "description": "test",
        "info": "test",
        "username": "test_test",
    }
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    client.put("/accounts/1/profile", json=json, headers=headers)

    account = session.execute(select(Account).where(Account.id == 1)).one_or_none().Account
    assert account.profile.avatar_id == 1
    assert account.profile.background_id == 1
    assert account.profile.description == "test"
    assert account.profile.info == "test"
    assert account.profile.username == "test_test"


def test_update_profile_returns_403_with_correct_body_when_query_account_does_not_coincide_with_token_account(
        client, token_for_testing, db_with_one_account_one_session,
):
    json = {
        "avatar_id": 1,
        "background_id": 1,
        "description": "test",
        "info": "test",
        "username": "test_test",
    }
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.put("/accounts/2/profile", json=json, headers=headers)

    assert response.status_code == 403
    assert response.json() == {"detail": "No rights to perform that action"}
