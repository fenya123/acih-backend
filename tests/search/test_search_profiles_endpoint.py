"""Tests for 'search_profiles' endpoint."""

from __future__ import annotations

import pytest


@pytest.mark.freeze_time("2024-06-09T14:31:36.577049Z")
def test_search_profiles_returns_200_with_correct_response(
    client,
    token_for_testing,
    db_with_three_accounts,
):
    headers = {"Authorization": f"Bearer {token_for_testing}"}

    response = client.get("/search/profiles?profile_username=test&limit=10&offset=0", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "profiles": [
            {
                "account_id": 1,
                "avatar_id": None,
                "background_id": None,
                "description": None,
                "info": None,
                "username": "test1",
                "created_at": "2024-06-09T14:31:36.577049Z",
            },
            {
                "account_id": 2,
                "avatar_id": None,
                "background_id": None,
                "description": None,
                "info": None,
                "username": "test12",
                "created_at": "2024-06-09T14:31:36.577049Z",
            },
            {
                "account_id": 3,
                "avatar_id": None,
                "background_id": None,
                "description": None,
                "info": None,
                "username": "test123",
                "created_at": "2024-06-09T14:31:36.577049Z",
            },
        ],
    }
