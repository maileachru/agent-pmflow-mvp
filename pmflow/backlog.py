from __future__ import annotations

from pathlib import Path

from .utils import slugify, today_iso, write_text


BACKLOG_TEMPLATE_DIR = Path("backlog/normalized")


def backlog_template(project_id: str, title: str) -> str:
    """Create a deterministic YAML backlog item template."""
    project_id = project_id.strip()
    title = title.strip()

    if not project_id:
        raise ValueError("project_id is required")
    if not title:
        raise ValueError("title is required")

    item_id = slugify(title)
    path = BACKLOG_TEMPLATE_DIR / f"{project_id}-{item_id}.yaml"
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
