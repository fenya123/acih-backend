"""Module contains tests for 'remove_session' endpoint."""

from __future__ import annotations


def test_remove_session_returns_204(client, db_with_one_account_one_session, token_for_testing):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.delete("/accounts/1/sessions/441d78c0-c031-4fa6-9f2a-78200da5c0fe", headers=headers)

    assert response.status_code == 204


def test_remove_session_returns_401_with_correct_body_when_token_has_invalid_signature(
    client, db_with_one_account_one_session, token_with_false_secret_key,
):
    headers = {"Authorization": f"Bearer {token_with_false_secret_key}"}

    response = client.delete("/accounts/1/sessions/441d78c0-c031-4fa6-9f2a-78200da5c0fe", headers=headers)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token."}


def test_remove_session_returns_401_with_correct_body_when_account_from_token_does_not_exist(
    client, db_empty, token_for_testing,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.delete("/accounts/1/sessions/441d78c0-c031-4fa6-9f2a-78200da5c0fe", headers=headers)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token."}


def test_remove_session_returns_401_with_correct_body_when_account_does_not_have_session_specified(
    client, db_with_one_account_one_other_session, token_for_testing,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.delete("/accounts/1/sessions/441d78c0-c031-4fa6-9f2a-78200da5c0fe", headers=headers)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token."}


def test_remove_session_returns_403_with_correct_body_when_query_account_does_not_coincide_with_token_account(
    client, db_with_one_account_one_session, token_for_testing,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.delete("/accounts/2/sessions/441d78c0-c031-4fa6-9f2a-78200da5c0fe", headers=headers)

    assert response.status_code == 403
    assert response.json() == {"detail": "No rights to perform that action"}


def test_remove_session_returns_403_with_correct_body_when_query_session_does_not_coincide_with_token_session(
    client, db_with_one_account_one_session, token_for_testing,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.delete("/accounts/1/sessions/6c0b95da-05e9-4bd5-8580-8695315b6785", headers=headers)

    assert response.status_code == 403
    assert response.json() == {"detail": "No rights to perform that action"}
