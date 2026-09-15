"""Provider-independent request, response, and tool-call types."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]


class ModelRequest(BaseModel):
    messages: list[dict[str, Any]]
    tools: list[ToolDefinition] = Field(default_factory=list)
    response_format: dict[str, Any] | None = None
    reasoning_effort: (
        Literal["none", "minimal", "low", "medium", "high", "xhigh", "max"] | None
    ) = None
    max_output_tokens: int | None = None
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: dict[str, Any]


class Usage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float | None = None


class ModelResponse(BaseModel):
    text: str | None = None
    tool_calls: list[ToolCall] = Field(default_factory=list)
    finish_reason: str | None = None
    model: str
    provider: str | None = None
    usage: Usage = Field(default_factory=Usage)
    request_id: str | None = None
    latency_ms: float | None = None
    mode: Literal["mock", "recorded", "live"]
