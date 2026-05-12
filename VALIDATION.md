# Validation

Validation for Agent PMFlow MVP (`agent-pmflow-mvp`).

## Required checks

Run before release:

```bash
pip install -e ".[dev]"
pmflow doctor
pmflow demo
pytest
```

## Latest local result

The required checks were run successfully during the production cleanup.

## Expected result

- Package installs as `agent-pmflow-mvp`.
- CLI command remains `pmflow`.
- `pmflow doctor` reports the CLI is ready.
- `pmflow demo` produces demo PM artifacts.
- `pytest` passes.
- Generated/cache files such as `*.egg-info/`, `__pycache__/`, `.pytest_cache/`, and `*.pyc` are ignored and not committed.
- Runtime PMFlow artifacts in `memory/` and `outputs/` are ignored unless intentionally promoted to curated examples.
