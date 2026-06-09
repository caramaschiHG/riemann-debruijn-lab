"""Robin and Lagarias criterion scans."""

from .robin_scan import RobinRecord, scan_robin
from .lagarias_scan import LagariasRecord, scan_lagarias

__all__ = ["RobinRecord", "LagariasRecord", "scan_robin", "scan_lagarias"]

