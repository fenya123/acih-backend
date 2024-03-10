"""Tests for 'remove_followee' endpoint."""

from __future__ import annotations

from sqlalchemy import select

from src.following.models import Following


def test_remove_followee_returns_204_and_deletes_db_entry(
    client, token_for_testing, db_with_several_following_relationsips,
):
    session = db_with_several_following_relationsips
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.delete("/accounts/1/followees/2", headers=headers)

    assert response.status_code == 204
    query = select(Following).where(Following.followee_id == 2, Following.follower_id == 1)
    result = session.execute(query).one_or_none()
    assert result is None


def test_remove_followee_returns_403_with_correct_response_when_follower_id_does_not_coincide_with_token_account(
    client, token_for_testing, db_with_several_following_relationsips,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.delete("/accounts/3/followees/2", headers=headers)

    assert response.status_code == 403
    assert response.json() == {"detail": "No rights to perform that action."}


def test_remove_followee_returns_404_with_correct_response_when_account_does_not_have_followee_with_id_provided(
    client, token_for_testing, db_with_several_following_relationsips,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.delete("/accounts/1/followees/10000", headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "No followee with that id."}
