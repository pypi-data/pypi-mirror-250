from typing import Optional

from pydantic import BaseModel

from pydantic_lambda_handler.main import PydanticLambdaHandler


def test_gen_event_model():
    """should work with an empty event"""

    class EventModel(BaseModel):
        path: dict[str, str]
        query: dict[str, str]
        body: Optional[dict[str, str]]

    PydanticLambdaHandler.parse_event_to_model({}, EventModel)


def test_base_url():
    url = PydanticLambdaHandler._generate_base_url(
        {
            "path": f"/resource/123/data",
            "requestContext": {
                "path": "/StageName/resource/123/data",
                "domainName": "test.example.com",
            },
        }
    )

    assert url == "https://test.example.com/StageName"
