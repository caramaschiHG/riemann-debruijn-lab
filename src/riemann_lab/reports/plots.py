"""Matplotlib plotting helpers."""

from __future__ import annotations

from pathlib import Path


def save_line_plot(path: Path | str, x: list[float], y: list[float], *, title: str, xlabel: str, ylabel: str) -> Path:
    """Save a simple line plot if matplotlib is available."""

    import matplotlib.pyplot as plt

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots()
    ax.plot(x, y, marker="o")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path

