# Reporting

Agent PMFlow MVP includes first-class reporting CLI commands. Reports are deterministic and read normalized backlog items from `backlog/normalized/*.yaml`.

## Inputs

Expected input backlog items:

```text
backlog/normalized/*.yaml
```

Each item must include `project_id`. Reporting commands filter by `project_id` and do not mix backlog items from different projects.

Optional executive-report inputs:

```text
backlog/reports/<project_id>-quality-report.md
backlog/roadmap/<project_id>-roadmap.md
outputs/status/*.md
outputs/*-manifest.txt
```

## Backlog quality report

```bash
pmflow backlog-report --project-id <project_id>
```

Generated output:

```text
backlog/reports/<project_id>-quality-report.md
```

Sections:

- Summary
- Total items
- Items by status
- Items by quarter
- Total confirmed estimate
- Items with missing estimate
- Items requiring clarification
- Items with risks
- Items requiring PGK approval
- Alumni-applicable items
- Recommendations

## Roadmap report

```bash
pmflow roadmap-report --project-id <project_id>
```

Generated output:

```text
backlog/roadmap/<project_id>-roadmap.md
```

The report groups backlog items by quarter and includes this table:

- ID
- Title
- Owner
- Priority
- Estimate
- Target End
- Status

## Executive report

```bash
pmflow executive-report --project-id <project_id> --title <title>
```

Generated output:

```text
outputs/reports/<project_id>-executive-report.md
```

The command uses available backlog quality report, roadmap report, latest weekly status, and latest manifest. Missing optional artifacts are marked as missing or not available.

Sections:

- Overall Status
- Key Dates
- Progress
- Risks / Blockers
- Decisions Needed
- Next Steps
- Attachments
