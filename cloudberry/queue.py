"""Upload queue helpers for offline and failed uploads."""

import json
import logging
import shutil
from pathlib import Path

logger = logging.getLogger("Cloudberry")

PENDING_DIR_NAME = "pending"
FAILED_DIR_NAME = "failed"
QUEUE_FILE_NAME = ".upload-queue.json"


def queue_paths(image_dir: Path) -> tuple[Path, Path, Path]:
    pending = image_dir / PENDING_DIR_NAME
    failed = image_dir / FAILED_DIR_NAME
    queue_file = image_dir / QUEUE_FILE_NAME
    pending.mkdir(parents=True, exist_ok=True)
    failed.mkdir(parents=True, exist_ok=True)
    return pending, failed, queue_file


def load_queue(queue_file: Path) -> list[str]:
    if not queue_file.exists():
        return []
    try:
        data = json.loads(queue_file.read_text(encoding="utf-8"))
        return [str(item) for item in data.get("files", [])]
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Could not read upload queue %s: %s", queue_file, exc)
        return []


def save_queue(queue_file: Path, files: list[Path]) -> None:
    payload = {"files": [str(path) for path in files]}
    queue_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def mark_failed(image_path: Path, failed_dir: Path) -> Path:
    destination = failed_dir / image_path.name
    if image_path.resolve() != destination.resolve():
        shutil.move(str(image_path), destination)
    return destination


def collect_upload_candidates(
    image_dir: Path,
    *,
    include_failed: bool = False,
) -> list[Path]:
    pending, failed, queue_file = queue_paths(image_dir)
    candidates: list[Path] = []

    for directory in (image_dir, pending):
        for path in sorted(directory.iterdir()):
            if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg"}:
                candidates.append(path)

    for queued in load_queue(queue_file):
        queued_path = Path(queued)
        if queued_path.exists() and queued_path not in candidates:
            candidates.append(queued_path)

    if include_failed:
        for path in sorted(failed.iterdir()):
            if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg"}:
                candidates.append(path)

    return candidates
