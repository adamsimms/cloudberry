"""Load rig secrets from environment or secrets.env (never committed)."""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATHS = (
    REPO_ROOT / "secrets.env",
    Path.home() / ".cloudberry" / "secrets.env",
)


def _load_secrets_file(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_secrets() -> None:
    explicit = os.environ.get("CLOUDBERRY_SECRETS_FILE")
    if explicit:
        _load_secrets_file(Path(explicit).expanduser())
        return
    for path in DEFAULT_PATHS:
        _load_secrets_file(path)


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Missing {name}. Copy .env.example to secrets.env and fill in values."
        )
    return value


def aws_credentials() -> tuple[str, str, str]:
    load_secrets()
    return (
        require_env("AWS_ACCESS_KEY_ID"),
        require_env("AWS_SECRET_ACCESS_KEY"),
        require_env("AWS_S3_BUCKET"),
    )


def gopro_wifi_password() -> str:
    load_secrets()
    return require_env("GOPRO_WIFI_PASSWORD")


def gopro_mac_address() -> str:
    load_secrets()
    return os.environ.get("GOPRO_MAC_ADDRESS", "AA:BB:CC:DD:EE:FF")
