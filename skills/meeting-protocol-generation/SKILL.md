# Meeting Protocol Generation

## Purpose

Convert meeting notes, transcript, or chat export into PM artifacts.

## Inputs

- Markdown meeting notes
- Transcript
- Telegram/chat export

## Outputs

- `/memory/meetings/<title>-protocol.md`
- `/memory/decisions/<title>-decisions.md`
- `/memory/actions/<title>-actions.md`
- `/outputs/presentations/<title>-outline.md`

## Rules

- Do not hallucinate decisions.
- If owner or due date is missing, use `TBD`.
- Keep output concise and operational.
- Put unresolved items into Open Questions.
