from __future__ import annotations

from pathlib import Path
import re

from .models import ActionItem, Decision
from .utils import read_text, write_text, slugify, today_iso


ACTION_PATTERNS = [
    r"(?P<owner>[A-ZА-ЯЁ][A-Za-zА-Яа-яЁё]+)\s+will\s+(?P<task>.+?)(?:\s+by\s+(?P<due>.+))?$",
    r"(?P<owner>[A-ZА-ЯЁ][A-Za-zА-Яа-яЁё]+)\s+должен\s+(?P<task>.+?)(?:\s+до\s+(?P<due>.+))?$",
    r"(?P<owner>[A-ZА-ЯЁ][A-Za-zА-Яа-яЁё]+)\s+подготовит\s+(?P<task>.+?)(?:\s+до\s+(?P<due>.+))?$",
    r"(?P<owner>[A-ZА-ЯЁ][A-Za-zА-Яа-яЁё]+)\s+сделает\s+(?P<task>.+?)(?:\s+до\s+(?P<due>.+))?$",
    r"(?P<owner>[A-ZА-ЯЁ][A-Za-zА-Яа-яЁё]+)\s+review\s+(?P<task>.+?)(?:\s+by\s+(?P<due>.+))?$",
]


def _clean_line(line: str) -> str:
    return line.strip().strip("-").strip()


def _extract_keyword_lines(text: str, keywords: list[str]) -> list[str]:
    result: list[str] = []
    for line in text.splitlines():
        clean = _clean_line(line)
        lower = clean.lower()
        if clean and any(k.lower() in lower for k in keywords):
            result.append(clean)
    return result


def extract_decisions(text: str, today: str) -> list[Decision]:
    lines = _extract_keyword_lines(text, ["decision:", "решение:", "decided", "решили"])
    decisions: list[Decision] = []
    for line in lines:
        cleaned = re.sub(r"^(decision:|решение:)\s*", "", line, flags=re.IGNORECASE)
        decisions.append(Decision(text=cleaned, date=today))
    return decisions


def extract_risks(text: str) -> list[str]:
    lines = _extract_keyword_lines(text, ["risk:", "риск:", "blocker", "blocked", "блокер"])
    return [re.sub(r"^(risk:|риск:)\s*", "", x, flags=re.IGNORECASE) for x in lines]


def extract_open_questions(text: str) -> list[str]:
    lines = _extract_keyword_lines(text, ["open question", "вопрос:", "should ", "нужно ли"])
    return [re.sub(r"^(open question:|вопрос:)\s*", "", x, flags=re.IGNORECASE) for x in lines]


def extract_actions(text: str) -> list[ActionItem]:
    actions: list[ActionItem] = []

    candidate_lines = _extract_keyword_lines(
        text,
        [
            " will ",
            "должен",
            "подготовит",
            "prepare",
            "review",
            "сделает",
            " by ",
            " до ",
        ],
    )

    for line in candidate_lines:
        lower = line.lower()
        if lower.startswith(("decision:", "решение:", "risk:", "риск:", "open question:", "вопрос:")):
            continue

        for pattern in ACTION_PATTERNS:
            match = re.search(pattern, line)
            if match:
                owner = match.groupdict().get("owner") or "TBD"
                task = match.groupdict().get("task") or line
                due = match.groupdict().get("due") or "TBD"
                actions.append(ActionItem(task=task.strip("."), owner=owner, due_date=due.strip(".")))
                break

    return actions


def process_meeting(input_path: str, title: str | None = None) -> dict[str, str]:
    source = read_text(input_path)
    slug = slugify(title or Path(input_path).stem)
    today = today_iso()

    decisions = extract_decisions(source, today)
    risks = extract_risks(source)
    actions = extract_actions(source)
    open_questions = extract_open_questions(source)

    decisions_bullets = "\n".join(f"- {d.text}" for d in decisions) if decisions else "- TBD"
    risks_bullets = "\n".join(f"- {r}" for r in risks) if risks else "- None identified"
    open_questions_bullets = "\n".join(f"- {q}" for q in open_questions) if open_questions else "- None"

    actions_rows = (
        "\n".join(f"| {a.task} | {a.owner} | {a.due_date} | {a.status} |" for a in actions)
        if actions
        else "| TBD | TBD | TBD | Open |"
    )

    decisions_rows = (
        "\n".join(f"| {d.text} | {d.rationale} | {d.owner} | {d.date} |" for d in decisions)
        if decisions
        else "| TBD | TBD | TBD | TBD |"
    )

    protocol = f"""
# {slug} — Meeting Protocol

## Summary

Meeting processed from `{input_path}` on {today}.

## Context

{source.strip()}

## Decisions

{decisions_bullets}

## Action Items

| Task | Owner | Due Date | Status |
|---|---|---|---|
{actions_rows}

## Risks / Blockers

{risks_bullets}

## Open Questions

{open_questions_bullets}

## Next Meeting

TBD
"""

    decisions_md = f"""
# {slug} — Decisions

| Decision | Rationale | Owner | Date |
|---|---|---|---|
{decisions_rows}
"""

    actions_md = f"""
# {slug} — Action Items

| Task | Owner | Due Date | Status |
|---|---|---|---|
{actions_rows}
"""

    outline = f"""
# {slug} — Presentation Outline

## Slide 1 — Executive Summary
- Weekly PM workflow processed
- Core artifacts generated
- Telegram draft and PowerPoint deck are available

## Slide 2 — Current Status
- Meeting protocol generated
- Decisions and actions extracted
- Weekly status prepared

## Slide 3 — Key Decisions
{chr(10).join(f"- {d.text}" for d in decisions[:5]) if decisions else "- TBD"}

## Slide 4 — Risks / Blockers
{chr(10).join(f"- {r}" for r in risks[:5]) if risks else "- No major risks identified"}

## Slide 5 — Next Steps
{chr(10).join(f"- {a.owner}: {a.task}" for a in actions[:5]) if actions else "- Define next actions"}

## Slide 6 — Decisions Required
- Confirm owners and due dates
- Confirm Telegram send policy
- Confirm next reporting cycle
"""

    outputs = {
        "protocol": f"memory/meetings/{slug}-protocol.md",
        "decisions": f"memory/decisions/{slug}-decisions.md",
        "actions": f"memory/actions/{slug}-actions.md",
        "outline": f"outputs/presentations/{slug}-outline.md",
    }

    write_text(outputs["protocol"], protocol)
    write_text(outputs["decisions"], decisions_md)
    write_text(outputs["actions"], actions_md)
    write_text(outputs["outline"], outline)

    return outputs
