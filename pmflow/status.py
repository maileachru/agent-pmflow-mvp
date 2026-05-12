from __future__ import annotations

from pathlib import Path

from .utils import write_text, slugify, today_iso, safe_title_suffix


def generate_weekly_status(
    title: str = "weekly-status",
    actions_path: str | None = None,
    decisions_path: str | None = None,
) -> str:
    slug = slugify(title)
    status_slug = safe_title_suffix(slug, "weekly-status")

    actions = Path(actions_path).read_text(encoding="utf-8") if actions_path and Path(actions_path).exists() else ""
    decisions = Path(decisions_path).read_text(encoding="utf-8") if decisions_path and Path(decisions_path).exists() else ""

    content = f"""
# {slug} — Weekly Status

Date: {today_iso()}

## Overall Status

Status: Yellow

## Completed

- Meeting protocol generated
- Decisions extracted
- Action items extracted
- Telegram reminder draft generated
- PowerPoint deck generated

## In Progress

{actions.strip() if actions.strip() else "- No action items found"}

## Risks / Blockers

- Telegram sending requires manual approval
- Owners and due dates may require human confirmation

## Decisions Needed

{decisions.strip() if decisions.strip() else "- No decisions found"}

## Next Steps

- Review action items
- Confirm owners and due dates
- Send Telegram reminders if approved
- Use PPTX for stakeholder update
"""
    output = f"outputs/status/{status_slug}.md"
    return write_text(output, content)
