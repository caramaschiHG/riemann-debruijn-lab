"""Markdown report helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from riemann_lab.constants import report_warning_block


def markdown_report(
    title: str,
    *,
    input_data: str,
    precision_notes: str,
    parameters: dict[str, object],
    results: list[str],
    interpretation: str,
    limitations: list[str] | None = None,
    next_steps: list[str] | None = None,
) -> str:
    """Build a standard markdown report with mandatory warnings."""

    lines = [
        f"# {title}",
        "",
        f"Date/time: {datetime.now(timezone.utc).isoformat()}",
        "",
        report_warning_block(),
        "",
        "## Input Data",
        input_data,
        "",
        "## Precision Notes",
        precision_notes or "No additional precision note supplied.",
        "",
        "## Parameters",
    ]
    lines.extend(f"- {key}: {value}" for key, value in parameters.items())
    lines.extend(["", "## Results"])
    lines.extend(f"- {item}" for item in results)
    lines.extend(["", "## Interpretation", interpretation, "", "## Limitations"])
    for item in limitations or ["Finite numerical computation only."]:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Steps"])
    for item in next_steps or ["Review assumptions before using results in a stronger claim."]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def write_markdown(path: Path | str, text: str) -> Path:
    """Write markdown text to a path."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path

