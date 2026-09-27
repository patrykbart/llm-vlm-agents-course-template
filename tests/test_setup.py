import json

from agent_project import MockClient, append_trace


def test_mock_client() -> None:
    client = MockClient([{"text": "hello", "tool_calls": [], "usage": {}}])
    assert client.complete([{"role": "user", "content": "Hi"}])["text"] == "hello"


def test_trace_redacts_secrets(tmp_path) -> None:
    path = tmp_path / "trace.jsonl"
    append_trace(path, "test", {"token": "secret", "value": 7})
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["payload"] == {"token": "[REDACTED]", "value": 7}
