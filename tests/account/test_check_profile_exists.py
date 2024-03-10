"""Module contains tests for 'profile_account_exists' endpoint."""

from __future__ import annotations


def test_check_profile_exists_returns_200_with_correct_response(
    client, db_with_one_account,
):
    response = client.get("/profiles/exists?username=test")

    assert response.status_code == 200
    assert response.json() == {"exists": True}
