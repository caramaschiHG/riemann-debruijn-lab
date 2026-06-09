import os
import subprocess
import sys
from pathlib import Path


def test_cli_help() -> None:
    root = Path(__file__).resolve().parents[1]
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root / "src")
    commands = [
        [],
        ["robin-scan"],
        ["lehmer-scan"],
        ["certify-tail"],
        ["uncertainty-stress"],
        ["gap-energy"],
        ["finite-flow"],
        ["report"],
        ["compare-candidates"],
    ]

    for command in commands:
        proc = subprocess.run(
            [sys.executable, "-m", "riemann_lab.cli", *command, "--help"],
            cwd=root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr
        assert "usage:" in proc.stdout
