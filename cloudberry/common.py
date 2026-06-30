"""Shared helpers for Cloudberry."""

from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path

import xmltodict


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


def parse_media_page(content: bytes | str) -> list[dict]:
    if isinstance(content, bytes):
        content = content.decode("utf-8", errors="replace")
    data = xmltodict.parse(content)
    tr_list = data["html"]["body"]["div"]["div"]["table"]["tbody"]["tr"]
    if not isinstance(tr_list, list):
        tr_list = [tr_list]
    images = []
    for tr in tr_list:
        entry: dict = {}
        for td in tr["td"]:
            if "a" in td:
                link = td["a"]
                entry["name"] = link["#text"] if isinstance(link, dict) else str(link)
            elif "span" in td and not isinstance(td["span"], list):
                span = td["span"]
                text = span["#text"] if isinstance(span, dict) else str(span)
                entry["date"] = datetime.strptime(text, "%d-%b-%Y %H:%M")
        if entry.get("name") and (".JPG" in entry["name"] or ".MP4" in entry["name"]):
            images.append(entry)
    return sorted(images, key=lambda img: img["name"])
