"""Configuration loading for Cloudberry."""

import configparser
import os
import shutil
from pathlib import Path

from cloudberry.secrets import aws_credentials, load_secrets

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "config.ini"
EXAMPLE_CONFIG = REPO_ROOT / "config.ini.example"

_config = configparser.ConfigParser()

VALID_CAMERA_TYPES = {"H3", "H4", "PICAMERA"}


def get_config_path() -> Path:
    env_path = os.environ.get("CLOUDBERRY_CONFIG")
    if env_path:
        return Path(env_path).expanduser()
    return DEFAULT_CONFIG


def ensure_config() -> Path:
    config_path = get_config_path()
    if config_path.exists():
        return config_path

    if EXAMPLE_CONFIG.exists():
        shutil.copy(EXAMPLE_CONFIG, config_path)
        print(f"No config file found. Copied {EXAMPLE_CONFIG} to {config_path}")
        return config_path

    raise FileNotFoundError(
        f"Config not found at {config_path}. Copy {EXAMPLE_CONFIG} to get started."
    )


def _read_config() -> None:
    config_path = ensure_config()
    _config.read(config_path)


def get_config(section: str, option: str, default=None):
    _read_config()
    try:
        return _config.get(section=section, option=option)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default


def get_bool_config(section: str, option: str, default: bool = False) -> bool:
    value = get_config(section, option)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_section_config(section: str = "picamera") -> dict[str, str]:
    _read_config()
    if section not in _config:
        return {}
    return {opt: _config.get(section, opt) for opt in _config.options(section)}


def normalize_camera_type(value: str | None) -> str:
    camera_type = (value or "H4").strip().upper()
    if camera_type not in VALID_CAMERA_TYPES:
        raise ValueError(f"Unsupported camera_type '{value}'. Use H3, H4, or picamera.")
    return camera_type


def get_camera_type() -> str:
    return normalize_camera_type(get_config("general", "camera_type", "H4"))


def get_aws_credentials() -> tuple[str, str, str]:
    load_secrets()
    try:
        key, secret, bucket = aws_credentials()
        return bucket, key, secret
    except RuntimeError:
        return "", "", ""


def get_aws_region() -> str | None:
    load_secrets()
    return os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
