# Getting Started

Agent PMFlow MVP (`agent-pmflow-mvp`) keeps the CLI command as `pmflow`.

## 1. Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 2. Verify

```bash
pmflow doctor
```

## 3. Run demo

```bash
pmflow demo
```

## 4. Process a real meeting

Put a markdown file into:

```text
meetings/inbox/
```

Example:

```bash
pmflow run-weekly   --meeting meetings/inbox/product-sync.md   --title product-sync
```

## 5. Outputs

Generated automatically:

```text
memory/meetings/
memory/decisions/
memory/actions/
outputs/status/
outputs/telegram/
outputs/presentations/
```
