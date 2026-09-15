"""Deterministic clients for development and grading."""

import json
from collections import deque
from pathlib import Path

from agent_course.types import ModelRequest, ModelResponse


class MockClient:
    def __init__(self, responses: list[ModelResponse]) -> None:
        self._responses = deque(responses)

    def generate(self, request: ModelRequest) -> ModelResponse:
        del request
        if not self._responses:
            raise RuntimeError("Mock response queue is empty")
        return self._responses.popleft()


class RecordedClient:
    def __init__(self, fixture: Path) -> None:
        records = json.loads(fixture.read_text(encoding="utf-8"))
        self._client = MockClient(
            [ModelResponse.model_validate(record) for record in records]
        )

    def generate(self, request: ModelRequest) -> ModelResponse:
        return self._client.generate(request)
