import json

import pytest
from demo_app_handlers import create_handler  # type: ignore


def test_get_response(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    response = requests_client.get(f"{base_url}/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_post_response(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    body = {"name": "Foo", "description": "An optional description", "price": 45.2, "tax": 3.5}
    response = requests_client.post(f"{base_url}/hello", json=body)
    assert response.status_code == 201, response.json()
    assert response.json() == body


def test_post_invalid_body(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    body = {
        "description": "An optional description",
        "price": 45.2,
    }
    response = requests_client.post(f"{base_url}/hello", json=body)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {"description": "An optional description", "price": 45.2},
                "loc": ["body", "name"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            }
        ]
    }


def test_post_invalid_empty_json(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    response = requests_client.post(f"{base_url}/hello", json="")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"class_name": "Item"},
                "input": "",
                "loc": ["body"],
                "msg": "Input should be a valid dictionary or instance of Item",
                "type": "model_type",
                "url": "https://errors.pydantic.dev/2.5/v/model_type",
            }
        ]
    }


def test_post_invalid_json(requests_client, base_url):
    """
    test that the message is returned to the body
    """
    response = create_handler({"path": f"{base_url}/hello", "body": "{"}, None)
    assert response["statusCode"] == 400
    assert json.loads(response["body"]) == {"detail": "JSONDecodeError"}


def test_inv(mock_lambda_context):
    event = {
        "resource": "/hello",
        "path": "/hello",
        "httpMethod": "POST",
        "queryStringParameters": None,
        "body": '{"name": "Foo", "description": "An optional description", "price": 45.2, "tax": 3.5}',
        "isBase64Encoded": False,
    }

    response = create_handler(event, mock_lambda_context)

    assert response["statusCode"] == 201, response.get("body")


def test_list_response(requests_client, base_url):
    response = requests_client.get(f"{base_url}/list_response")
    assert response.status_code == 200
    assert response.json() == [{"item_name": 1}]


@pytest.mark.xfail(reason="Partial upgrade to pydantic v2")
def test_list_response_model(requests_client, base_url):
    response = requests_client.get(f"{base_url}/list_response_model")
    assert response.status_code == 200
    assert response.json() == [{"item_name": "secret", "item_value": None}]


def test_error_much_handler(requests_client, base_url):
    response = requests_client.get(f"{base_url}/error_much")
    assert response.status_code == 502
    assert response.json() == {"message": "Internal server error"}


def test_error_much_handler_post(requests_client, base_url):
    response = requests_client.post(f"{base_url}/error_much")
    assert response.status_code == 502
    assert response.json() == {"message": "Internal server error"}
