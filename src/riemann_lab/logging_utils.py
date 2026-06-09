"""Logging setup for command line experiments."""

from __future__ import annotations

import logging


def get_logger(name: str = "riemann_lab", verbose: bool = False) -> logging.Logger:
    """Return a console logger with a stable format."""

    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    return logger

