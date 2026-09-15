"""Run a small, identical compatibility suite against both candidate models."""

import argparse
import base64
import json
from collections.abc import Callable
from pathlib import Path
from statistics import mean
from typing import Any

from pydantic import BaseModel

from agent_course.client import OpenRouterClient
from agent_course.config import ModelMode, Settings
from agent_course.tracing import append_trace
from agent_course.types import ModelRequest, ToolDefinition

CANDIDATES = (
    "google/gemma-4-26b-a4b-it",
    "qwen/qwen3.6-35b-a3b",
)


class Classification(BaseModel):
    category: str
    confidence: float


def exact_answer(client: OpenRouterClient) -> tuple[bool, str]:
    response = client.generate(
        ModelRequest(
            messages=[
                {
                    "role": "user",
                    "content": "Reply with exactly COURSE_READY and nothing else.",
                }
            ],
            reasoning_effort="none",
            max_output_tokens=32,
        )
    )
    return response.text == "COURSE_READY", response.model_dump_json()


def structured_output(client: OpenRouterClient) -> tuple[bool, str]:
    schema = Classification.model_json_schema()
    response = client.generate(
        ModelRequest(
            messages=[
                {
                    "role": "user",
                    "content": "Classify 'The build failed' as success or failure.",
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "classification",
                    "strict": True,
                    "schema": schema,
                },
            },
            reasoning_effort="none",
            max_output_tokens=128,
        )
    )
    try:
        parsed = Classification.model_validate_json(response.text or "")
    except ValueError:
        return False, response.model_dump_json()
    return parsed.category == "failure", response.model_dump_json()


def tool_call(client: OpenRouterClient) -> tuple[bool, str]:
    response = client.generate(
        ModelRequest(
            messages=[
                {
                    "role": "user",
                    "content": "Use multiply exactly once to calculate 6 times 7.",
                }
            ],
            tools=[
                ToolDefinition(
                    name="multiply",
                    description="Multiply two integers.",
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
            reasoning_effort="none",
            max_output_tokens=128,
        )
    )
    valid = len(response.tool_calls) == 1
    if valid:
        call = response.tool_calls[0]
        valid = call.name == "multiply" and call.arguments in (
            {"a": 6, "b": 7},
            {"a": 7, "b": 6},
        )
    return valid, response.model_dump_json()


def vision(client: OpenRouterClient) -> tuple[bool, str]:
    image_path = Path(__file__).parent.parent / "fixtures/images/course-diagram.png"
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    response = client.generate(
        ModelRequest(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "What number is inside the blue box? "
                                "Reply only with the number."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{encoded}"},
                        },
                    ],
                }
            ],
            reasoning_effort="none",
            max_output_tokens=32,
        )
    )
    return (response.text or "").strip() == "42", response.model_dump_json()


CASES: dict[str, Callable[[OpenRouterClient], tuple[bool, str]]] = {
    "instruction": exact_answer,
    "structured_output": structured_output,
    "tool_call": tool_call,
    "vision": vision,
}


def run_model(model: str, repetitions: int, trace_path: Path) -> dict[str, Any]:
    settings = Settings(model_mode=ModelMode.LIVE, model_name=model)
    client = OpenRouterClient(settings)
    rows: list[dict[str, Any]] = []
    for _ in range(repetitions):
        for name, case in CASES.items():
            try:
                passed, response_json = case(client)
                response = json.loads(response_json)
                row = {
                    "model": model,
                    "case": name,
                    "passed": passed,
                    "latency_ms": response.get("latency_ms"),
                    "cost_usd": response.get("usage", {}).get("cost_usd"),
                    "response": response,
                }
            except Exception as error:  # benchmark records provider failures
                row = {
                    "model": model,
                    "case": name,
                    "passed": False,
                    "error": f"{type(error).__name__}: {error}",
                }
            rows.append(row)
            append_trace(trace_path, "benchmark_case", row)

    costs = [row["cost_usd"] for row in rows if row.get("cost_usd") is not None]
    latencies = [row["latency_ms"] for row in rows if row.get("latency_ms") is not None]
    return {
        "model": model,
        "passed": sum(bool(row["passed"]) for row in rows),
        "total": len(rows),
        "pass_rate": sum(bool(row["passed"]) for row in rows) / len(rows),
        "cost_usd": sum(costs) if costs else None,
        "mean_latency_ms": mean(latencies) if latencies else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--trace", type=Path, default=Path("traces/benchmark.jsonl"))
    args = parser.parse_args()
    if not 1 <= args.repetitions <= 20:
        raise SystemExit("--repetitions must be between 1 and 20")

    results = [run_model(model, args.repetitions, args.trace) for model in CANDIDATES]
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
