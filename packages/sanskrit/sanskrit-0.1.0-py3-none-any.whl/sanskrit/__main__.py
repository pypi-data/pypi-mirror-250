"""Support executing the CLI by doing `python -m sanskrit`."""
from __future__ import annotations

from sanskrit.cli import cli

if __name__ == "__main__":
    raise SystemExit(cli())
