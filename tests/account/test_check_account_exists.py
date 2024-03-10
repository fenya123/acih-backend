"""Module contains tests for 'check_account_exists' endpoint."""

from __future__ import annotations


def test_check_account_exists_returns_200_with_correct_response(
    client, db_with_one_account,
):
    response = client.get("/accounts/exists?email=test@gmail.com")

    assert response.status_code == 200
    assert response.json() == {"exists": True}
