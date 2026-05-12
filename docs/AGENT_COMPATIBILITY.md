# Agent Compatibility

Agent PMFlow MVP uses plain Markdown instructions and a normal CLI so it can be used by Codex today and adapted to other agents later.

## Compatibility Strategy

The repository has three portable layers:

1. `AGENTS.md` — the high-level operating contract.
2. `skills/<skill>/SKILL.md` — focused PM workflows.
3. `pmflow` CLI — deterministic artifact generation.

Agents should read the instruction layer, choose the smallest required skill, and run the CLI instead of inventing a new process.

## Codex

Codex is the primary target for this MVP.

Recommended prompt:

```text
Read AGENTS.md.
Use the smallest required PM skill.
Run pmflow run-weekly --meeting meetings/inbox/product-sync.md --title product-sync.
Do not send Telegram messages.
```

## Claude Code

Use this repository as a project folder or plugin-style instruction pack. Keep `AGENTS.md` and `skills/*/SKILL.md` as the source of truth. Ask Claude Code to run the same `pmflow` commands rather than creating alternate workflows.

## Cursor

Reference the relevant `SKILL.md` files as project rules. For routine use, keep `AGENTS.md` as the top-level rule and copy only the needed PM skill into Cursor rules if context must be smaller.

## Gemini CLI

Use `AGENTS.md` as persistent project context and point Gemini CLI at the `skills/` directory when a PM workflow is requested. The command contract remains `pmflow`.

## Windsurf

Add the contents of `AGENTS.md` and the relevant `skills/<skill>/SKILL.md` to Windsurf rules. Do not add IDE-specific automation unless it preserves the same folder contracts.

## OpenCode

Use the repository-native `AGENTS.md` flow. The agent should load exactly one or more relevant PM skills and write artifacts into the documented output folders.

## GitHub Copilot

Use `AGENTS.md` as repository instructions and place summaries of the PM skills in Copilot custom instructions if needed. Copilot should not send Telegram messages; it should generate drafts only.

## Kiro IDE & CLI

Mirror the `skills/` folder into Kiro skill locations if desired. Keep the PMFlow CLI as the execution layer.

## Other Agents

Any agent that can read Markdown and run shell commands can use this project:

```bash
pmflow doctor
pmflow run-weekly --meeting meetings/inbox/product-sync.md --title product-sync
```

## Non-Goal

This project is not a multi-agent platform. Compatibility means the same Markdown skills and CLI can be reused, not that the repository orchestrates multiple agents.
