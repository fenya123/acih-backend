"""Module contains tests for 'create_session' endpoint."""

from __future__ import annotations

from datetime import datetime

import dirty_equals
import jwt
from sqlalchemy import select

from src.auth.enums import Algorithm
from src.auth.models import Session
from src.config import config


def test_create_session_returns_201_with_correct_response(client, db_with_one_account):
    session = db_with_one_account

    response = client.post("/sessions", json={"email": "test@gmail.com", "password": "testpassword"})

    assert response.status_code == 201
    auth_session = session.query(Session).one()
    assert response.json() == {
        "session": {
            "id": dirty_equals.IsUUID(4),
            "account_id": 1,
            "created_at": auth_session.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        },
        "token": dirty_equals.IsStr,
    }
    token = response.json()["token"]
    payload = jwt.decode(token, config.SECRET_KEY, Algorithm.HS256.value)
    assert payload == {
        "account_id": 1,
        "session_id": dirty_equals.IsUUID(4),
    }


def test_create_session_creates_session_in_db_correctly(client, db_with_one_account):
    session = db_with_one_account

    response = client.post("/sessions", json={"email": "test@gmail.com", "password": "testpassword"})  # noqa: F841

    auth_session = session.execute(select(Session)).one().Session
    assert auth_session.id == dirty_equals.IsUUID(4)
    assert auth_session.account_id == 1
    assert isinstance(auth_session.created_at, datetime)


def test_create_session_returns_404_when_account_with_provided_email_does_not_exist(client, db_with_one_account):
    response = client.post("/sessions", json={"email": "test1@gmail.com", "password": "testpassword"})

    assert response.status_code == 404
    assert response.json() == {
        "resource": "Account",
        "description": "Requested resource not found.",
        "detail": "Requested resource doesn't exist or has been deleted.",
    }


def test_create_session_returns_404_when_account_with_provided_password_does_not_exist(client, db_with_one_account):
    response = client.post("/sessions", json={"email": "test@gmail.com", "password": "testpassword1"})

    assert response.status_code == 404
    assert response.json() == {
        "resource": "Account",
        "description": "Requested resource not found.",
        "detail": "Requested resource doesn't exist or has been deleted.",
    }
