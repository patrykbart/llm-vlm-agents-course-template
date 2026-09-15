"""Live OpenRouter adapter behind a small course-owned protocol."""

import json
import time
from typing import Any, Protocol

from openai import OpenAI

from agent_course.config import Settings
from agent_course.types import ModelRequest, ModelResponse, ToolCall, Usage


class ModelClient(Protocol):
    def generate(self, request: ModelRequest) -> ModelResponse:
        """Return assistant text and any requested tool calls."""


class OpenRouterClient:
    def __init__(self, settings: Settings) -> None:
        settings.require_live_credentials()
        self.settings = settings
        self._client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.model_base_url,
        )

    def generate(self, request: ModelRequest) -> ModelResponse:
        payload: dict[str, Any] = {
            "model": self.settings.model_name,
            "messages": request.messages,
            "temperature": request.temperature,
            "max_tokens": request.max_output_tokens or self.settings.max_output_tokens,
        }
        if request.tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": tool.model_dump(),
                }
                for tool in request.tools
            ]
        if request.response_format is not None:
            payload["response_format"] = request.response_format
        payload["extra_body"] = {"usage": {"include": True}}

        started = time.perf_counter()
        completion = self._client.chat.completions.create(**payload)
        latency_ms = (time.perf_counter() - started) * 1000
        message = completion.choices[0].message

        tool_calls = []
        for call in message.tool_calls or []:
            try:
                arguments = json.loads(call.function.arguments)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON arguments for tool {call.function.name}"
                ) from error
            tool_calls.append(
                ToolCall(id=call.id, name=call.function.name, arguments=arguments)
            )

        raw_usage = completion.usage
        return ModelResponse(
            text=message.content,
            tool_calls=tool_calls,
            finish_reason=completion.choices[0].finish_reason,
            model=completion.model,
            usage=Usage(
                input_tokens=getattr(raw_usage, "prompt_tokens", 0),
                output_tokens=getattr(raw_usage, "completion_tokens", 0),
                cost_usd=getattr(raw_usage, "cost", None),
            ),
            request_id=completion.id,
            latency_ms=latency_ms,
            mode="live",
        )
