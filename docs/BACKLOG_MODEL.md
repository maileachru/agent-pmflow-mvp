# Universal Backlog Model

The backlog model extends Agent PMFlow MVP from meeting/status automation to universal backlog management for any project.

## Why `project_id` Is Required

`project_id` is a required core field because this repository can store backlog items for multiple projects at the same time. A stable project identifier prevents accidental mixing of unrelated roadmap items, reports, and normalized files.

Examples:

- `pulse-youth-alumni`
- `internal-platform`
- `customer-portal`

Every backlog item must include `project_id`. Do not create normalized backlog files without it.

## Core Fields

Normalized backlog items use `backlog/schema/backlog-item.schema.yaml` and include:

- `id` — stable item identifier within the project
- `project_id` — required project identifier
- `title` — short human-readable item name
- `description` — item summary
- `type` — normalized item type
- `status` — normalized workflow status
- `priority` — normalized priority
- `owner` — responsible person or `TBD`
- `estimate` — estimate value and unit
- `dates` — created, updated, start, due, and quarter fields
- `acceptance_criteria` — measurable acceptance checks
- `definition_of_done` — completion requirements
- `success_metrics` — outcome metrics
- `dependencies` — blocking or sequencing dependencies
- `risks` — known delivery risks
- `open_questions` — unresolved questions
- `custom_fields` — project-specific source fields

## `custom_fields` Examples

Keep root fields universal. Put project-specific fields in `custom_fields`, for example:

```yaml
custom_fields:
  alumni_applicable: true
  pgk_required: false
  artifact: backlog-source
  source_quarter: Q2 2026
  comment: Imported from project-specific planning table.
```

Fields such as `alumni_applicable`, `pgk_required`, and `source_quarter` must not be added as root schema fields.

## Status Values

Use only these normalized statuses:

- `new`
- `ready`
- `in_progress`
- `blocked`
- `done`
- `canceled`

If the source status is unclear, use `new` and preserve the original value in `custom_fields.source_status`.

## Type Values

Use only these normalized types:

- `epic`
- `feature`
- `story`
- `task`
- `bug`
- `research`
- `milestone`

If the source type is unclear, use `task` and preserve the original value in `custom_fields.source_type`.

## Example Item

```yaml
id: pulse-events-module
project_id: pulse-youth-alumni
title: Модуль Мероприятия
description: Единый модуль для публикации и управления мероприятиями проекта.
type: feature
status: new
priority: high
owner: TBD
estimate:
  value: TBD
  unit: tbd
dates:
  created: null
  updated: null
  start: null
  due: null
  quarter: 2026-Q2
acceptance_criteria:
  - Можно создать мероприятие с названием, описанием, датой и ответственным.
definition_of_done:
  - Требования согласованы с владельцем проекта.
success_metrics:
  - Сокращено ручное сопровождение мероприятий.
dependencies: []
risks: []
open_questions: []
custom_fields:
  alumni_applicable: true
  pgk_required: false
  artifact: backlog-source
  source_quarter: Q2 2026
  comment: Перенесено в универсальную модель backlog item.
```

## Recommended CSV Columns

For simple imports, use these CSV columns:

```text
id,project_id,title,description,type,status,priority,owner,estimate_value,estimate_unit,created,updated,start,due,quarter,acceptance_criteria,definition_of_done,success_metrics,dependencies,risks,open_questions,custom_fields
```

Project-specific columns may also be present in the source CSV, but normalized YAML files should place them under `custom_fields`.
