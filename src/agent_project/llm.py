"""Minimal live and mock model clients. Build your agent around this interface."""

import os
from collections import deque
from typing import Any, Protocol

from dotenv import load_dotenv
from openai import OpenAI


class ModelClient(Protocol):
    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]: ...


class OpenRouterClient:
    def __init__(self, model: str | None = None) -> None:
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = model or os.getenv("MODEL_NAME")
        if not api_key or not self.model:
            raise ValueError("Set OPENROUTER_API_KEY and MODEL_NAME in .env")
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        request: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
            "extra_body": {"usage": {"include": True}},
        }
        if tools:
            request["tools"] = tools

        response = self.client.chat.completions.create(**request)
        message = response.choices[0].message
        return {
            "text": message.content,
            "tool_calls": [
                {
                    "id": call.id,
                    "name": call.function.name,
                    "arguments": call.function.arguments,
                }
                for call in message.tool_calls or []
            ],
            "usage": response.usage.model_dump() if response.usage else {},
        }


class MockClient:
    def __init__(self, responses: list[dict[str, Any]]) -> None:
        self.responses = deque(responses)

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        del messages, tools
        if not self.responses:
            raise RuntimeError("Mock response queue is empty")
        return self.responses.popleft()
