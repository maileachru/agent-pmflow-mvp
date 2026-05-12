from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import re

from .utils import safe_title_suffix, slugify, today_iso, write_text


@dataclass(frozen=True)
class PlanningItem:
    task: str
    owner: str
    due_date: str
    status: str


def _parse_iso_date(value: str) -> date | None:
    clean = value.strip()
    if not clean or clean.upper() == "TBD":
        return None
    for pattern in (r"\d{4}-\d{2}-\d{2}", r"\d{4}/\d{2}/\d{2}"):
        match = re.search(pattern, clean)
        if not match:
            continue
        normalized = match.group(0).replace("/", "-")
        try:
            return datetime.strptime(normalized, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def _parse_actions_table(actions_markdown: str) -> list[PlanningItem]:
    items: list[PlanningItem] = []
    for line in actions_markdown.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped or "Task" in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 4:
            continue
        task, owner, due_date, status = cells[:4]
        if task and task.upper() != "TBD":
            items.append(PlanningItem(task=task, owner=owner or "TBD", due_date=due_date or "TBD", status=status or "Open"))
    return items


def _mermaid_task_name(item: PlanningItem) -> str:
    text = f"{item.owner}: {item.task}" if item.owner != "TBD" else item.task
    return text.replace(":", "-").replace("#", "").strip()


def generate_gantt(title: str = "project-plan", actions_path: str | None = None) -> str:
    """Generate a deterministic Mermaid Gantt markdown artifact from action items.

    Only ISO-like due dates (`YYYY-MM-DD` or `YYYY/MM/DD`) are scheduled. Non-date
    due values remain visible in an unscheduled table for human PM review.
    """

    slug = slugify(title)
    gantt_slug = safe_title_suffix(slug, "gantt")
    today = datetime.strptime(today_iso(), "%Y-%m-%d").date()

    actions = Path(actions_path).read_text(encoding="utf-8") if actions_path and Path(actions_path).exists() else ""
    items = _parse_actions_table(actions)

    scheduled: list[tuple[PlanningItem, date]] = []
    unscheduled: list[PlanningItem] = []
    for item in items:
        due = _parse_iso_date(item.due_date)
        if due:
            scheduled.append((item, due))
        else:
            unscheduled.append(item)

    scheduled.sort(key=lambda pair: (pair[1], pair[0].owner, pair[0].task))
    unscheduled.sort(key=lambda item: (item.owner, item.task))

    if scheduled:
        mermaid_rows = "\n".join(
            f"    {_mermaid_task_name(item)} :active, {index}, {today.isoformat()}, {due.isoformat()}"
            for index, (item, due) in enumerate(scheduled, start=1)
        )
    else:
        mermaid_rows = f"    No ISO-dated actions yet :milestone, m1, {today.isoformat()}, 0d"

    scheduled_rows = (
        "\n".join(
            f"| {item.task} | {item.owner} | {due.isoformat()} | {item.status} |"
            for item, due in scheduled
        )
        if scheduled
        else "| None | TBD | TBD | TBD |"
    )
    unscheduled_rows = (
        "\n".join(f"| {item.task} | {item.owner} | {item.due_date} | {item.status} |" for item in unscheduled)
        if unscheduled
        else "| None | TBD | TBD | TBD |"
    )

    content = f"""
# {slug} — Gantt Plan

Generated from `{actions_path or 'no actions file'}` on {today.isoformat()}.

## Mermaid Gantt

```mermaid
gantt
    title {slug} plan
    dateFormat  YYYY-MM-DD
    axisFormat  %Y-%m-%d
    section Scheduled Actions
{mermaid_rows}
```

## Scheduled Actions

| Task | Owner | Due Date | Status |
|---|---|---|---|
{scheduled_rows}

## Unscheduled / Needs PM Review

These items are not placed on the Gantt timeline until the PM confirms an ISO due date (`YYYY-MM-DD`).

| Task | Owner | Due Date | Status |
|---|---|---|---|
{unscheduled_rows}
"""

    return write_text(f"outputs/planning/{gantt_slug}.md", content)
