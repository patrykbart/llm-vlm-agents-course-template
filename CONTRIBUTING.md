# Contributing

This repository is distributed to students as a GitHub template. Changes to
shared starter code should preserve deterministic offline tests and must not
introduce credentials, personal data, or live API calls into CI.

Before proposing a change, run:

```bash
uv run ruff check .
uv run pytest
```

Instructor benchmark traces are local artifacts and must not be committed.
