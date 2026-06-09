"""Minimal LaTeX report helpers."""

from __future__ import annotations


def markdown_to_simple_latex(markdown_text: str) -> str:
    """Convert a small markdown report to a plain LaTeX verbatim document."""

    escaped = markdown_text.replace("\\", "\\textbackslash{}").replace("&", "\\&")
    return "\\documentclass{article}\n\\begin{document}\n\\begin{verbatim}\n" + escaped + "\n\\end{verbatim}\n\\end{document}\n"

