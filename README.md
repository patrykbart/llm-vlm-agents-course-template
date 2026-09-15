# Designing LLM/VLM Agents — Student Starter

Starter repository for the five-meeting course **Designing LLM/VLM Agents**.
Students extend a small, provider-independent agent runtime while working with
tool calling, MCP, retrieval, vision, evaluation, and safety.

## What You Need

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Git
- an individual course OpenRouter key supplied by the instructor
- Docker before Meeting 4, unless a hosted sandbox is provided

A local model and a coding agent are not required.

## Setup

```bash
git clone https://github.com/patrykbart/llm-vlm-agents-course-template.git
cd llm-vlm-agents-course-template
uv sync
cp .env.example .env
uv run pytest
```

Insert your individual key in `.env`, then run the connection check:

```bash
uv run python -m agent_course.check_openrouter
```

Never commit `.env` or paste a course key into source code, an issue, a report,
or a shared document.

## Execution Modes

- `mock`: deterministic unit tests and error cases; no network or API cost.
- `recorded`: replay instructor-provided responses; no network or API cost.
- `live`: use the allowlisted course model through OpenRouter.

Use mock or recorded mode while developing. Use live mode only for required
behavioural experiments.

## Course Limits

- one instructor-selected model, with no fallback model;
- USD 2 total OpenRouter allowance per student;
- USD 0.10 maximum per agent run;
- eight model steps per run by default; and
- only supplied, public, or synthetic data.

## Repository Map

```text
assignments/             meeting-specific starter work
data/                    supplied public or synthetic course data
fixtures/                deterministic model responses and images
src/agent_course/        shared model adapter, tracing, and safety code
tests/                   deterministic tests
instructor/              benchmark documentation; no credentials
```

Start with [Meeting 1](assignments/meeting_01/README.md).

## Submission Expectations

Every submission must include:

- working source code;
- tests;
- machine-readable JSON Lines traces;
- a short engineering note explaining design decisions and limitations;
- measured live-run cost where required; and
- disclosure of any coding-agent assistance, according to course policy.

You must be able to explain and modify every submitted component.

## Licence

Course starter code is released under the MIT License. Assignment instructions
and teaching materials remain attributed to the course author.
