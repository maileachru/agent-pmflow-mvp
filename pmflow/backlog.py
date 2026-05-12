from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .utils import slugify, today_iso, write_text


BACKLOG_TEMPLATE_DIR = Path("backlog/normalized")
BACKLOG_REPORT_DIR = Path("backlog/reports")
ROADMAP_DIR = Path("backlog/roadmap")
EXECUTIVE_REPORT_DIR = Path("outputs/reports")


def backlog_template(project_id: str, title: str) -> str:
    """Create a deterministic YAML backlog item template."""
    project_id = project_id.strip()
    title = title.strip()

    if not project_id:
        raise ValueError("project_id is required")
    if not title:
        raise ValueError("title is required")

    item_id = slugify(title)
    path = BACKLOG_TEMPLATE_DIR / f"{project_id}-backlog-item.yaml"
    content = f"""
id: {item_id}
project_id: {project_id}
title: {title}
description: TBD
type: task
status: new
priority: medium
owner: TBD
estimate:
  value: TBD
  unit: tbd
dates:
  created: {today_iso()}
  updated: null
  start: null
  due: null
  quarter: null
acceptance_criteria: []
definition_of_done: []
success_metrics: []
dependencies: []
risks: []
open_questions: []
custom_fields: {{}}
"""
    return write_text(path, content)


def generate_backlog_report(project_id: str) -> str:
    """Generate a deterministic backlog quality report for one project."""
    project_id = _require_project_id(project_id)
    items = _load_project_items(project_id)

    by_status = Counter(_scalar(item.get("status"), "TBD") for item in items)
    by_quarter = Counter(_nested_scalar(item, "dates", "quarter", "Unscheduled") for item in items)
    missing_estimate = [item for item in items if _missing_estimate(item)]
    needs_clarification = [item for item in items if _list_value(item.get("open_questions"))]
    with_risks = [item for item in items if _list_value(item.get("risks"))]
    pgk_items = [item for item in items if _truthy(_nested_value(item, "custom_fields", "pgk_required"))]
    alumni_items = [item for item in items if _truthy(_nested_value(item, "custom_fields", "alumni_applicable"))]

    content = f"""
# Backlog Quality Report — {project_id}

## Summary

Project `{project_id}` has {len(items)} backlog item(s) in `backlog/normalized`.

{_item_table(items)}

## Total items

{len(items)}

## Items by status

{_count_table(by_status, 'Status')}

## Items by quarter

{_count_table(by_quarter, 'Quarter')}

## Total confirmed estimate

{_confirmed_estimate_summary(items)}

## Items with missing estimate

{_item_table(missing_estimate)}

## Items requiring clarification

{_item_table(needs_clarification)}

## Items with risks

{_item_table(with_risks)}

## Items requiring PGK approval

{_item_table(pgk_items)}

## Alumni-applicable items

{_item_table(alumni_items)}

## Recommendations

{_recommendations(missing_estimate, needs_clarification, with_risks, pgk_items)}
"""
    return write_text(BACKLOG_REPORT_DIR / f"{project_id}-quality-report.md", content)


def generate_roadmap_report(project_id: str) -> str:
    """Generate a quarter-grouped roadmap for one project."""
    project_id = _require_project_id(project_id)
    items = _load_project_items(project_id)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[_nested_scalar(item, "dates", "quarter", "Unscheduled")].append(item)

    sections = []
    for quarter in sorted(grouped):
        rows = [_roadmap_row(item) for item in sorted(grouped[quarter], key=lambda i: _scalar(i.get("id")))]
        sections.append(f"## {quarter}\n\n| ID | Title | Owner | Priority | Estimate | Target End | Status |\n| --- | --- | --- | --- | --- | --- | --- |\n" + "\n".join(rows))

    content = f"""
# Roadmap Report — {project_id}

{chr(10).join(sections) if sections else '_No backlog items found for this project._'}
"""
    return write_text(ROADMAP_DIR / f"{project_id}-roadmap.md", content)


def generate_executive_report(project_id: str, title: str) -> str:
    """Generate an executive report using existing product artifacts when available."""
    project_id = _require_project_id(project_id)
    title = title.strip()
    if not title:
        raise ValueError("title is required")

    quality_path = BACKLOG_REPORT_DIR / f"{project_id}-quality-report.md"
    roadmap_path = ROADMAP_DIR / f"{project_id}-roadmap.md"
    weekly_status = _latest_file(Path("outputs/status"), "*.md")
    manifest = _latest_file(Path("outputs"), "*-manifest.txt")
    items = _load_project_items(project_id)
    blockers = [item for item in items if _scalar(item.get("status")) == "blocked"]
    risks = [item for item in items if _list_value(item.get("risks"))]
    decisions_needed = [item for item in items if _list_value(item.get("open_questions"))]

    content = f"""
# Executive Report — {title}

## Overall Status

{_overall_status(items, blockers, risks)}

## Key Dates

{_key_dates(items)}

## Progress

{_progress_summary(items, weekly_status)}

## Risks / Blockers

{_risk_summary(blockers, risks)}

## Decisions Needed

{_item_table(decisions_needed)}

## Next Steps

- Review items requiring clarification.
- Confirm missing estimates before roadmap commitment.
- Resolve PGK approvals before implementation start.

## Attachments

- Backlog quality report: `{quality_path}` ({'available' if quality_path.exists() else 'missing'})
- Roadmap report: `{roadmap_path}` ({'available' if roadmap_path.exists() else 'missing'})
- Latest weekly status: `{weekly_status}`
- Latest manifest: `{manifest}`
"""
    return write_text(EXECUTIVE_REPORT_DIR / f"{project_id}-executive-report.md", content)


def _require_project_id(project_id: str) -> str:
    project_id = project_id.strip()
    if not project_id:
        raise ValueError("project_id is required")
    return project_id


def _load_project_items(project_id: str) -> list[dict[str, Any]]:
    items = [_parse_simple_yaml(path) for path in sorted(BACKLOG_TEMPLATE_DIR.glob("*.yaml"))]
    return [item for item in items if _scalar(item.get("project_id")) == project_id]


def _parse_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_map: str | None = None
    current_list: str | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if indent == 0 and ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_map = None
            current_list = None
            if value == "":
                data[key] = {}
                current_map = key
            elif value == "[]":
                data[key] = []
                current_list = key
            elif value == "{}":
                data[key] = {}
                current_map = key
            else:
                data[key] = _parse_scalar(value)
        elif indent == 2 and line.startswith("- ") and (current_list or current_map):
            list_key = current_list or current_map
            values = data.setdefault(list_key, [])
            if not isinstance(values, list):
                values = []
                data[list_key] = values
            values.append(_parse_scalar(line[2:].strip()))
        elif indent == 2 and current_map and ":" in line:
            key, value = line.split(":", 1)
            nested = data.setdefault(current_map, {})
            if isinstance(nested, dict):
                nested[key.strip()] = _parse_scalar(value.strip())
    return data


def _parse_scalar(value: str) -> Any:
    if value in {"null", "~"}:
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def _scalar(value: Any, default: str = "TBD") -> str:
    if value is None or value == "":
        return default
    return str(value)


def _nested_value(item: dict[str, Any], parent: str, key: str) -> Any:
    nested = item.get(parent)
    if isinstance(nested, dict):
        return nested.get(key)
    return None


def _nested_scalar(item: dict[str, Any], parent: str, key: str, default: str) -> str:
    return _scalar(_nested_value(item, parent, key), default)


def _list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() in {"true", "yes", "1"}


def _missing_estimate(item: dict[str, Any]) -> bool:
    value = _nested_value(item, "estimate", "value")
    unit = _nested_value(item, "estimate", "unit")
    return value in {None, "", "TBD", "tbd"} or unit in {None, "", "tbd"}


def _confirmed_estimate_summary(items: list[dict[str, Any]]) -> str:
    totals: dict[str, float] = defaultdict(float)
    for item in items:
        value = _nested_value(item, "estimate", "value")
        unit = _nested_scalar(item, "estimate", "unit", "tbd")
        if isinstance(value, (int, float)) and unit != "tbd":
            totals[unit] += float(value)
    if not totals:
        return "No confirmed estimates."
    return ", ".join(f"{total:g} {unit}" for unit, total in sorted(totals.items()))


def _count_table(counter: Counter[str], label: str) -> str:
    if not counter:
        return "_No items._"
    rows = [f"| {label} | Count |", "| --- | ---: |"]
    rows.extend(f"| {key} | {counter[key]} |" for key in sorted(counter))
    return "\n".join(rows)


def _item_table(items: list[dict[str, Any]]) -> str:
    if not items:
        return "_None._"
    rows = ["| ID | Title | Status |", "| --- | --- | --- |"]
    rows.extend(f"| {_scalar(item.get('id'))} | {_scalar(item.get('title'))} | {_scalar(item.get('status'))} |" for item in items)
    return "\n".join(rows)


def _roadmap_row(item: dict[str, Any]) -> str:
    estimate = f"{_nested_scalar(item, 'estimate', 'value', 'TBD')} {_nested_scalar(item, 'estimate', 'unit', 'tbd')}"
    return " | ".join([
        "| " + _scalar(item.get("id")),
        _scalar(item.get("title")),
        _scalar(item.get("owner")),
        _scalar(item.get("priority")),
        estimate,
        _nested_scalar(item, "dates", "due", "TBD"),
        _scalar(item.get("status")) + " |",
    ])


def _recommendations(missing: list[dict[str, Any]], clarification: list[dict[str, Any]], risks: list[dict[str, Any]], pgk: list[dict[str, Any]]) -> str:
    recommendations = []
    if missing:
        recommendations.append("- Add confirmed estimates for items before roadmap commitment.")
    if clarification:
        recommendations.append("- Resolve open questions for items requiring clarification.")
    if risks:
        recommendations.append("- Review risk-bearing items with owners.")
    if pgk:
        recommendations.append("- Schedule PGK approval for required items.")
    return "\n".join(recommendations) if recommendations else "- No immediate backlog quality actions."


def _latest_file(directory: Path, pattern: str) -> str:
    files = sorted(directory.glob(pattern), key=lambda path: (path.stat().st_mtime, path.name)) if directory.exists() else []
    return str(files[-1]) if files else "not available"


def _overall_status(items: list[dict[str, Any]], blockers: list[dict[str, Any]], risks: list[dict[str, Any]]) -> str:
    if blockers:
        return f"Attention needed: {len(blockers)} blocked item(s) and {len(risks)} item(s) with risks."
    if risks:
        return f"On track with watch items: {len(risks)} item(s) have risks."
    return f"On track: {len(items)} backlog item(s) reviewed."


def _key_dates(items: list[dict[str, Any]]) -> str:
    dated = [item for item in items if _nested_value(item, "dates", "due")]
    if not dated:
        return "_No target dates available._"
    rows = ["| Item | Target End | Quarter |", "| --- | --- | --- |"]
    for item in sorted(dated, key=lambda i: _nested_scalar(i, "dates", "due", "")):
        rows.append(f"| {_scalar(item.get('id'))} | {_nested_scalar(item, 'dates', 'due', 'TBD')} | {_nested_scalar(item, 'dates', 'quarter', 'Unscheduled')} |")
    return "\n".join(rows)


def _progress_summary(items: list[dict[str, Any]], weekly_status: str) -> str:
    by_status = Counter(_scalar(item.get("status"), "TBD") for item in items)
    status_text = ", ".join(f"{status}: {count}" for status, count in sorted(by_status.items())) or "no backlog items"
    return f"Backlog status distribution: {status_text}. Latest weekly status: `{weekly_status}`."


def _risk_summary(blockers: list[dict[str, Any]], risks: list[dict[str, Any]]) -> str:
    combined = {str(item.get("id")): item for item in blockers + risks}
    return _item_table(list(combined.values()))
