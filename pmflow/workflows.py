from __future__ import annotations

from pathlib import Path

from .utils import slugify, write_text
from .processor import process_meeting
from .status import generate_weekly_status
from .telegram import generate_reminders, send_file_text
from .pptx_export import export_pptx
from .gantt import generate_gantt


def run_weekly(
    meeting: str,
    title: str | None = None,
    send_telegram: bool = False,
    dry_run: bool = False,
    no_pptx: bool = False,
    telegram_message_limit: int = 20,
) -> dict[str, str]:
    if not Path(meeting).exists():
        raise FileNotFoundError(f"Meeting file not found: {meeting}")

    slug = slugify(title or Path(meeting).stem)

    outputs = process_meeting(meeting, slug)

    status_path = generate_weekly_status(
        title=slug,
        actions_path=outputs["actions"],
        decisions_path=outputs["decisions"],
    )

    telegram_draft_path = generate_reminders(
        outputs["actions"],
        message_limit=telegram_message_limit,
    )

    gantt_path = generate_gantt(slug, outputs["actions"])

    result = {
        **outputs,
        "weekly_status": status_path,
        "telegram_draft": telegram_draft_path,
        "gantt": gantt_path,
        "telegram_sent": "false",
    }

    if no_pptx:
        result["pptx"] = "skipped"
    else:
        result["pptx"] = export_pptx(
            outline_path=outputs["outline"],
            output_path=f"outputs/presentations/{slug}.pptx",
        )

    if send_telegram:
        send_file_text(telegram_draft_path, dry_run=dry_run)
        result["telegram_sent"] = "dry-run" if dry_run else "true"

    manifest = "\n".join(f"{key}: {value}" for key, value in result.items())
    result["manifest"] = write_text(f"outputs/{slug}-manifest.txt", manifest)

    return result
