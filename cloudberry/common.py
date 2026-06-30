"""Shared helpers for Cloudberry."""

from __future__ import annotations

import sys
import time
from pathlib import Path


def count_down(seconds: int) -> None:
    for remaining in range(seconds, 0, -1):
        print(remaining)
        sys.stdout.flush()
        time.sleep(1)
    print()


def get_serial() -> str:
    serial = "0000000000000000"
    cpuinfo = Path("/proc/cpuinfo")
    if not cpuinfo.exists():
        return serial

    try:
        for line in cpuinfo.read_text(encoding="utf-8").splitlines():
            if line.startswith("Serial"):
                serial = line.split(":", 1)[1].strip().lstrip("0") or "0"
                break
    except OSError:
        return "ERROR000000000"

    return serial
