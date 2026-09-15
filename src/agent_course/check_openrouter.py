"""Minimal live connection and tool-calling diagnostic."""

from agent_course.client import OpenRouterClient
from agent_course.config import Settings
from agent_course.types import ModelRequest, ToolDefinition


def main() -> None:
    settings = Settings()
    client = OpenRouterClient(settings)
    response = client.generate(
        ModelRequest(
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Call the add tool exactly once to calculate 19 + 23. "
                        "Do not calculate it yourself."
                    ),
                }
            ],
            tools=[
                ToolDefinition(
                    name="add",
                    description="Add two integers.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "a": {"type": "integer"},
                            "b": {"type": "integer"},
                        },
                        "required": ["a", "b"],
                        "additionalProperties": False,
                    },
                )
            ],
            max_output_tokens=128,
        )
    )
    if len(response.tool_calls) != 1:
        raise SystemExit("Expected exactly one tool call")
    call = response.tool_calls[0]
    if call.name != "add" or call.arguments != {"a": 19, "b": 23}:
        raise SystemExit(f"Unexpected tool call: {call.model_dump()}")
    print(
        "Connection check passed:",
        response.model,
        f"{response.usage.input_tokens} input tokens,",
        f"{response.usage.output_tokens} output tokens,",
        f"{response.latency_ms:.0f} ms",
    )


if __name__ == "__main__":
    main()
