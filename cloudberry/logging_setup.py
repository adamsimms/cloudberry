"""Programmatic logging setup with absolute paths and rotation."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG_DIR = REPO_ROOT / "logs"
LOG_FORMAT = "%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s"


def resolve_log_dir(configured: str | None = None) -> Path:
    if configured and configured.strip():
        log_dir = Path(configured).expanduser()
    else:
        log_dir = DEFAULT_LOG_DIR

    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def setup_logging(log_dir: Path | None = None, level: int = logging.DEBUG) -> logging.Logger:
    target_dir = log_dir or DEFAULT_LOG_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    log_file = target_dir / "cloudberry.log"

    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=20 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.WARNING)

    logger = logging.getLogger("Cloudberry")
    logger.handlers.clear()
    logger.setLevel(level)
    logger.propagate = False
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.debug("Logging to %s", log_file)
    return logger
