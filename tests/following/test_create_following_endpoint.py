"""Tests for 'create_following' endpoint."""

from __future__ import annotations

from sqlalchemy import select

from src.following.models import Following


def test_create_following_returns_201_with_correct_response(
    client, db_with_two_accounts_one_session, token_for_testing,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}
    json = {
        "follower_id": 1,
        "followee_id": 2,
    }

    response = client.post("/followings", headers=headers, json=json)

    assert response.status_code == 201
    assert response.json() == {
        "id": 10000,
        "follower_id": 1,
        "followee_id": 2,
    }


def test_create_following_returns_422_with_correct_response_when_following_self(
    client, db_with_two_accounts_one_session, token_for_testing,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}
    json = {
        "follower_id": 1,
        "followee_id": 1,
    }

    response = client.post("/followings", headers=headers, json=json)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"error": {}},
                "input": {"followee_id": 1, "follower_id": 1},
                "loc": ["body"],
                "msg": "Value error, Can't follow self.",
                "type": "value_error",
                "url": "https://errors.pydantic.dev/2.5/v/value_error",
            },
        ],
    }


def test_create_following_creates_correct_db_entry(
    client, db_with_two_accounts_one_session, token_for_testing,
):
    session = db_with_two_accounts_one_session
    headers = {"Authorization": f"Bearer {token_for_testing}"}
    json = {
        "follower_id": 1,
        "followee_id": 2,
    }

    client.post("/followings", headers=headers, json=json)

    following = session.execute(select(Following).where(Following.id == 10000)).one().Following
    assert following.follower_id == 1
    assert following.followee_id == 2


def test_create_following_returns_403_with_correct_response_when_follower_id_does_not_coincide_with_token_account(
    client, db_with_two_accounts_one_session, token_for_testing,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}
    json = {
        "follower_id": 10000,
        "followee_id": 2,
    }

    response = client.post("/followings", headers=headers, json=json)

    assert response.status_code == 403
    assert response.json() == {"detail": "No rights to perform that action"}


def test_create_following_returns_403_with_correct_response_when_following_already_exists(
    client, db_with_two_accounts_one_session_one_following, token_for_testing,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}
    json = {
        "follower_id": 1,
        "followee_id": 2,
    }

    response = client.post("/followings", headers=headers, json=json)

    assert response.status_code == 403
    assert response.json() == {"detail": "Already following."}


def test_create_following_returns_404_with_correct_response_when_followee_does_not_exist(
    client, db_with_one_account_one_session, token_for_testing,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}
    json = {
        "follower_id": 1,
        "followee_id": 2,
    }

    response = client.post("/followings", headers=headers, json=json)

    assert response.status_code == 404
    assert response.json() == {"detail": "Account not found"}
