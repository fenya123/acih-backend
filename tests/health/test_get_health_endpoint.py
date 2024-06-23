"""Module for testing 'root' endpoint."""

from __future__ import annotations


def test_get_health_endpoint_returns_200_with_correct_response(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
