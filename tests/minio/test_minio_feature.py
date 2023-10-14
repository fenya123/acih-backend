from __future__ import annotations


def test_add_object_returns_200_and_adds_objects_to_storage(client, storage_empty):
    response = client.post("/objects/testobject1")

    assert response.status_code == 200
    assert storage_empty.bucket_exists("testbucket")
    assert len(list(storage_empty.list_objects("testbucket"))) > 0


def test_get_object_list_with_non_empty_storage_returns_200_with_correct_data(
    client,
    storage_with_one_bucket_one_object,
):
    response = client.get("/objects")

    assert response.status_code == 200
    assert response.json() == {
        "objects": [
            {"name": "testobject", "size": 12},
        ],
    }
