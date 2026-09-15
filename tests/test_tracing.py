import json

from agent_course.tracing import append_trace


def test_trace_redacts_secrets(tmp_path) -> None:
    trace = tmp_path / "trace.jsonl"
    append_trace(
        trace,
        "request",
        {"authorization": "Bearer secret", "safe": {"value": 7}},
    )

    record = json.loads(trace.read_text(encoding="utf-8"))
    assert record["payload"]["authorization"] == "[REDACTED]"
    assert record["payload"]["safe"] == {"value": 7}
