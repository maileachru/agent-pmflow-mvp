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

Use one Markdown meeting note, transcript, or chat export as the input artifact. Put it into:

```text
meetings/inbox/
```

Recommended source shape:

```markdown
Decision: We will run a limited pilot.
Anna will publish the pilot charter by 2026-05-13.
Risk: Data export may be delayed.
Open question: Should partners see confidence scores?
```

Example:

```bash
pmflow run-weekly --meeting meetings/inbox/product-sync.md --title product-sync
```

## 5. Outputs

Generated automatically from that one meeting input:

```text
memory/meetings/
memory/decisions/
memory/actions/
outputs/status/
outputs/telegram/
outputs/planning/
outputs/presentations/
```


## 6. Movement through artifacts

For the complete input contract, artifact handoff map, and manual one-artifact commands, read `docs/ARTIFACT_FLOW.md`.
