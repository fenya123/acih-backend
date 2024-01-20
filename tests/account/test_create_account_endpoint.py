"""Module contains tests for 'create_account' endpoint."""

from __future__ import annotations

import hashlib

from src.account.enums import Algorithm
from src.account.models import Account, PasswordHash
from src.profile.models import Profile


def test_create_account_returns_201_with_correct_response(client):
    data = {
        "email": "Placeholder_AdDrEsS_for_test_123@gmail.com",
        "password": "Placeholder!Password?11233)_",
        "username": "testname123",
    }

    response = client.post("/accounts", json=data)

    assert response.status_code == 201
    assert response.json() == {
        "account": {
            "id": 10000,
            "email": "Placeholder_AdDrEsS_for_test_123@gmail.com",
        },
        "profile": {
            "account_id": 10000,
            "avatar_id": None,
            "background_id": None,
            "description": None,
            "info": None,
            "username": "testname123",
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
    assert len(session.query(Account).where(Account.email == "Placeholder_AdDrEsS_for_test_123@gmail.com").all()) == 1
    assert len(session.query(Profile).where(Profile.username == "testname123").all()) == 1
    assert len(session.query(PasswordHash).all()) == 1
    password_hash = session.query(PasswordHash).one()
    hash_object = hashlib.new(Algorithm.SHA256.value)
    salted_password = data["password"] + password_hash.salt
    hash_object.update(salted_password.encode("ascii"))
    assert password_hash.value == hash_object.hexdigest()
