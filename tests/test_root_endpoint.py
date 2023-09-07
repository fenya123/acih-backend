"""Module for testing 'root' endpoint."""

from __future__ import annotations


def test_root_endpiont_return_200_with_corrcet_response(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
