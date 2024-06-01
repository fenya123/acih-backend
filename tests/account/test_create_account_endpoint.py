"""Module contains tests for 'create_account' endpoint."""

from __future__ import annotations

import hashlib
from datetime import datetime

from src.account.enums import Algorithm
from src.account.models import Account, PasswordHash
from src.profile.models import Profile


def test_create_account_returns_201_with_correct_response(client, db_empty):
    session = db_empty
    data = {
        "email": "Placeholder_AdDrEsS_for_test_123@gmail.com",
        "password": "Placeholder!Password?11233)_",
        "username": "testname123",
    }

    response = client.post("/accounts", json=data)

    assert response.status_code == 201
    account = session.query(Account).one()
    assert response.json() == {
        "account": {
            "id": 10000,
            "email": "Placeholder_AdDrEsS_for_test_123@gmail.com",
            "created_at": account.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        },
        "profile": {
            "account_id": 10000,
            "avatar_id": None,
            "background_id": None,
            "description": None,
            "info": None,
            "username": "testname123",
            "created_at": account.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        },
    }


def test_create_account_adds_correct_data_to_db(client, db_empty):
    session = db_empty
    data = {
        "email": "Placeholder_AdDrEsS_for_test_123@gmail.com",
        "password": "Placeholder!Password?11233)_",
        "username": "testname123",
    }

    response = client.post("/accounts", json=data)

    assert response.status_code == 201
    account = session.query(Account).one()
    assert account.email == "Placeholder_AdDrEsS_for_test_123@gmail.com"
    assert isinstance(account.created_at, datetime)
    profile = session.query(Profile).one()
    assert profile.account_id == account.id
    assert isinstance(profile.created_at, datetime)
    assert len(session.query(PasswordHash).all()) == 1
    password_hash = session.query(PasswordHash).one()
    hash_object = hashlib.new(Algorithm.SHA256.value)
    salted_password = data["password"] + password_hash.salt
    hash_object.update(salted_password.encode("ascii"))
    assert password_hash.value == hash_object.hexdigest()
