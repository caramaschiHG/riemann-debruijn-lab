"""Fail on dangerous mathematical claim language in public docs/reports."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SCAN_PATHS = [
    ROOT / "README.md",
    ROOT / "REPRODUCIBILITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    ROOT / "docs",
    ROOT / "outputs" / "candidate_comparison",
    ROOT / "outputs" / "reproduction",
]

DANGEROUS_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bproved RH\b",
        r"\bproves RH\b",
        r"\bsolved RH\b",
        r"\bwe solved\b",
        r"\bproof of the Riemann Hypothesis\b",
        r"\bLambda <= 0 established\b",
    ]
]

CERTIFICATE_PATTERN = re.compile(r"\bcertificate\b", re.IGNORECASE)
CERTIFICATE_ALLOWED_CONTEXT = re.compile(
    r"assumption|conditional|future|not |review|language|requires|would be required|rigorous-certificate|before",
    re.IGNORECASE,
)

TEXT_EXTENSIONS = {".md", ".txt", ".csv"}


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in SCAN_PATHS:
        if not path.exists():
            continue
        if path.is_file():
            files.append(path)
        else:
            files.extend(child for child in path.rglob("*") if child.is_file())
    return sorted(
        path
        for path in files
        if path.suffix.lower() in TEXT_EXTENSIONS
        and ".egg-info" not in path.parts
    )


def line_window(lines: list[str], index: int, radius: int = 2) -> str:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)
    return " ".join(lines[start:end])


def check_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    failures: list[str] = []
    for line_no, line in enumerate(lines, start=1):
        for pattern in DANGEROUS_PATTERNS:
            if not pattern.search(line):
                continue
            context = line_window(lines, line_no - 1)
            if re.search(r"does not|do not|not a|no ", context, re.IGNORECASE):
                continue
            failures.append(f"{path.relative_to(ROOT)}:{line_no}: dangerous phrase: {line.strip()}")
        if CERTIFICATE_PATTERN.search(line):
            context = line_window(lines, line_no - 1)
            if not CERTIFICATE_ALLOWED_CONTEXT.search(context):
                failures.append(
                    f"{path.relative_to(ROOT)}:{line_no}: 'certificate' lacks nearby assumptions/limitations: {line.strip()}"
                )
    return failures


def main() -> int:
    failures: list[str] = []
    for path in iter_files():
        failures.extend(check_file(path))
    if failures:
        print("Claim-language check failed:")
        for failure in failures:
            print(failure)
        return 1
    print("Claim-language check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
