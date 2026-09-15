# Instructor Material

This directory contains public benchmark definitions and documentation. It
must never contain OpenRouter management keys, student-key mappings, grading
records, or private student information.

Before distributing the template:

1. benchmark `google/gemma-4-26b-a4b-it` and `qwen/qwen3.6-35b-a3b`;
2. select exactly one model;
3. replace the placeholder `MODEL_NAME` in `.env.example`;
4. create student keys with a USD 2 limit and a one-model allowlist; and
5. run every assignment with an instructor-as-student key.

## Candidate Smoke Benchmark

Use an instructor test key that temporarily allows both candidate identifiers.
Set only `OPENROUTER_API_KEY` in `.env`; the benchmark overrides the student
model placeholder separately for each candidate.

Run a low-cost first pass:

```bash
uv run python instructor/benchmark.py --repetitions 3
```

The command tests exact instruction following, JSON Schema output, a typed tool
call, and a supplied image. It writes detailed local results to
`traces/benchmark.jsonl`, which is ignored by Git. This smoke suite verifies the
harness; expand it with the complete course evaluation set before freezing the
model choice.
