# My Agent Project

Student project for **Designing LLM/VLM Agents**.

## Setup

Create your own repository with **Use this template**, then clone your new
repository:

```bash
git clone <your-repository-url>
cd <your-repository-directory>
uv sync --locked
cp .env.example .env
uv run pytest
```

Add the individual OpenRouter key supplied by the instructor to `.env`. Never
commit this file or place the key in code, traces, issues, or reports.

## Project Brief

- **Project title:**
- **Intended user:**
- **Problem and primary task:**
- **Why an agent is appropriate:**
- **Planned data:**
- **Planned tools:**
- **Planned visual input:**
- **Success criteria:**
- **Non-goals and safety boundaries:**

Replace the empty fields above with your project definition and keep them
current as the project develops.

## Starter Code

The repository contains only:

- `src/agent_project/llm.py` — minimal OpenRouter and mock clients;
- `src/agent_project/tracing.py` — a JSON Lines trace helper;
- `tests/test_setup.py` — a setup check;
- `data/` — approved project data; and
- `traces/` — generated traces, which are ignored by Git.

The agent loop, domain tools, state, retrieval, multimodal behavior, evaluation,
and safety controls are intentionally left for you to design and implement.

## Commands

```bash
uv run pytest
uv run ruff check .
```

Use the assignments published on the course website as the source of truth.
