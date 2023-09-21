"""Module for testing entity related endpoints."""

from __future__ import annotations

from src.entity.models import Entity


def test_create_entity_returns_200_with_correct_response(client):
    response = client.post("/entities/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1}


def test_create_entity_adds_data_to_db(client, db_empty):
    session = db_empty

    client.post("/entities/1")

    assert len(session.query(Entity).all()) == 1
    assert session.query(Entity).first().id == 1


def test_get_entity_list_return_200_with_correct_response(client, db_with_one_entity):
    response = client.get("/entities")

    assert response.status_code == 200
    assert response.json() == {
        "entities": [
            {"id": 1},
        ],
    }
