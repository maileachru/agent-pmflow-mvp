from __future__ import annotations

from pathlib import Path
import re
from datetime import date


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9а-яё\-\s_]+", "", value, flags=re.IGNORECASE)
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-") or "pm-output"


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str | Path, content: str) -> str:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    return str(path)


def today_iso() -> str:
    return date.today().isoformat()


def markdown_table_rows(path: str | Path) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        if "---" in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if not parts:
            continue
        first = parts[0].lower()
        if first in {"task", "decision"}:
            continue
        rows.append(parts)
    return rows


def safe_title_suffix(title: str, suffix: str) -> str:
    slug = slugify(title)
    suffix = suffix.strip("-")
    if slug.endswith(f"-{suffix}"):
        return slug
    return f"{slug}-{suffix}"
