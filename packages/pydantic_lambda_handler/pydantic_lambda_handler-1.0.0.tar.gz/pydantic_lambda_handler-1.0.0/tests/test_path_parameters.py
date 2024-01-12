import pytest
from handler_app import plh


def test_path_parameters_without_typehint(requests_client, base_url):
    response = requests_client.get(f"{base_url}/pets/1")
    assert response.status_code == 200
    assert response.json() == {"pet_id": "1"}


def test_path_parameters_with_typehint(requests_client, base_url):
    response = requests_client.get(f"{base_url}/items/2")
    assert response.status_code == 200
    assert response.json() == {"item_id": 2}


def test_path_parameters_with_enum_typehint(requests_client, base_url):
    response = requests_client.get(f"{base_url}/item_enum/dog")
    assert response.status_code == 200
    assert response.json() == {"item_id": "dog"}


def test_path_parameters_with_typehint_typeerror(requests_client, base_url):
    response = requests_client.get(f"{base_url}/item_enum/cat")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"expected": "'dog'"},
                "input": "cat",
                "loc": ["path", "item_id"],
                "msg": "Input should be 'dog'",
                "type": "enum",
                "url": "https://errors.pydantic.dev/2.5/v/enum",
            }
        ]
    }


def test_path_parameters_with_path_default():
    # Fix me should only error on run otherwise we block
    # all the other handlers
    with pytest.raises(Exception):

        @plh.get("/items/{item_id}")
        def handler_with_path_default(item_id=2):
            return {"item_id": item_id}
