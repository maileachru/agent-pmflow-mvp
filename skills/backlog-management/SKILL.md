# Backlog Management Skill

Use this skill when the user asks to import, normalize, analyze, template, report, or plan backlog items.

## Scope

This skill supports universal backlog management for any project in this repository. Keep the workflow deterministic and minimal:

- store source files in `backlog/raw/`
- store one normalized YAML file per backlog item in `backlog/normalized/`
- store roadmap outputs in `backlog/roadmap/`
- store quality reports in `backlog/reports/`
- do not store backlog items in `memory/actions/`
- do not add Jira, Confluence, RAG, vector DB, email automation, or multi-agent logic

## Backlog Item Model

Every normalized backlog item must follow `backlog/schema/backlog-item.schema.yaml` and include these core fields:

- `id`
- `project_id`
- `title`
- `description`
- `type`
- `status`
- `priority`
- `owner`
- `estimate`
- `dates`
- `acceptance_criteria`
- `definition_of_done`
- `success_metrics`
- `dependencies`
- `risks`
- `open_questions`
- `custom_fields`

## `project_id` Rule

`project_id` is required for every backlog item. It must be a stable, repository-wide project identifier such as `pulse-youth-alumni`.

Never create or normalize a backlog item without `project_id`. If the source does not contain it, stop and request or infer a single explicit project id only when the user has provided enough context.

## `custom_fields` Rule

Keep the core model universal. Project-specific fields must go under `custom_fields`, not into the root schema.

Examples of project-specific fields that belong in `custom_fields`:

- `alumni_applicable`
- `pgk_required`
- `artifact`
- `source_quarter`
- `comment`

## Status Normalization

Normalize status values to this fixed set:

- `new` — captured but not ready for work
- `ready` — refined and ready to start
- `in_progress` — actively being worked on
- `blocked` — cannot progress until a dependency or question is resolved
- `done` — completed and accepted
- `canceled` — intentionally removed from scope

If a source status is unclear, use `new` and add the original status to `custom_fields.source_status`.

## Type Normalization

Normalize item types to this fixed set:

- `epic`
- `feature`
- `story`
- `task`
- `bug`
- `research`
- `milestone`

If a source type is unclear, use `task` and add the original type to `custom_fields.source_type`.

## Quarter Normalization

Normalize quarters in `dates.quarter` to `YYYY-QN`, for example `2026-Q2`.

If the source contains formats such as `Q2 2026`, `2Q26`, or `2026 / Q2`, normalize them to `2026-Q2` and keep the original value in `custom_fields.source_quarter` when useful.

## Creating Normalized Backlog Files

1. Read the raw source from `backlog/raw/` or save the user-provided source there first.
2. Determine the required `project_id` before creating normalized items.
3. Create one YAML file per item in `backlog/normalized/`.
4. Name files deterministically: `<project_id>-<item-id>.yaml`.
5. Include every core field, even when the value is `TBD`, `null`, or an empty list.
6. Put project-specific source columns in `custom_fields`.
7. Keep meeting follow-up actions separate in `memory/actions/`; backlog items never belong there.
