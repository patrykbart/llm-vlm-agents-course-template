from agent_course.offline import MockClient
from agent_course.types import ModelRequest, ModelResponse


def test_mock_client_returns_queued_response() -> None:
    expected = ModelResponse(text="hello", model="fixture", mode="mock")
    client = MockClient([expected])

    actual = client.generate(ModelRequest(messages=[]))

    assert actual == expected
