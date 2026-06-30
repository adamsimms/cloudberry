"""Configuration and environment validation."""

from __future__ import annotations

import re
import socket
from dataclasses import dataclass, field

from cloudberry.config import (
    get_aws_credentials,
    get_aws_region,
    get_camera_type,
    get_config,
    get_section_config,
)
from cloudberry.secrets import gopro_wifi_password, load_secrets

RESOLUTION_RE = re.compile(r"^\d+x\d+$", re.IGNORECASE)


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)


def validate_resolution(value: str) -> bool:
    if not RESOLUTION_RE.match(value):
        return False
    width, height = value.lower().split("x", 1)
    return int(width) > 0 and int(height) > 0


def validate_config() -> ValidationResult:
    result = ValidationResult()

    delay = get_config("general", "delay", "1")
    try:
        if int(delay) < 0:
            result.add_error("general.delay must be zero or positive")
    except ValueError:
        result.add_error("general.delay must be an integer")

    try:
        camera_type = get_camera_type()
        result.warnings.append(f"camera_type set to {camera_type}")
    except ValueError as exc:
        result.add_error(str(exc))
        camera_type = "H4"

    load_secrets()
    try:
        bucket, key, secret = get_aws_credentials()
        if not all([bucket, key, secret]):
            raise RuntimeError("incomplete")
    except RuntimeError:
        result.add_error(
            "AWS credentials missing. Copy .env.example to secrets.env and set "
            "AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET"
        )

    if camera_type in {"H3", "H4"}:
        try:
            gopro_wifi_password()
        except RuntimeError:
            result.add_error("GOPRO_WIFI_PASSWORD missing from secrets.env")

    if camera_type == "PICAMERA":
        resolution = get_config("picamera", "resolution", "2592x1944")
        if not validate_resolution(resolution):
            result.add_error("picamera.resolution must use WIDTHxHEIGHT format")

        camera_settings = get_section_config("picamera")
        for option in ("warmup_seconds", "jpeg_quality"):
            if option in camera_settings:
                try:
                    value = int(camera_settings[option])
                    if value < 0:
                        result.add_error(f"picamera.{option} must be zero or positive")
                except ValueError:
                    result.add_error(f"picamera.{option} must be an integer")

    return result


def check_network(host: str = "8.8.8.8", port: int = 53, timeout: float = 3.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def check_picamera_available() -> tuple[bool, str]:
    try:
        from picamera2 import Picamera2
    except ImportError:
        return False, "picamera2 is not installed"

    try:
        camera_ids = Picamera2.global_camera_info()
        if not camera_ids:
            return False, "no cameras detected by libcamera"
        return True, f"detected {len(camera_ids)} camera(s)"
    except Exception as exc:
        return False, f"camera probe failed: {exc}"


def check_gopro_reachable() -> tuple[bool, str]:
    ip = get_config("gopro", "ip", "10.5.5.9")
    try:
        with socket.create_connection((ip, 80), timeout=3.0):
            return True, f"GoPro reachable at {ip}"
    except OSError:
        return False, f"cannot reach GoPro at {ip} (Wi-Fi connected?)"


def check_s3_credentials(
    bucket: str,
    access_key: str,
    secret_key: str,
    region: str | None,
) -> tuple[bool, str]:
    try:
        import boto3
        from botocore.exceptions import BotoCoreError, ClientError

        client_kwargs = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
        }
        if region:
            client_kwargs["region_name"] = region

        client = boto3.client("s3", **client_kwargs)
        client.head_bucket(Bucket=bucket)
        return True, f"bucket '{bucket}' is reachable"
    except (BotoCoreError, ClientError, Exception) as exc:
        return False, f"S3 check failed: {exc}"


def run_preflight_checks(*, skip_camera: bool = False, skip_s3: bool = False) -> ValidationResult:
    result = ValidationResult()

    if not check_network():
        result.add_error("network preflight failed: unable to reach external network")
    else:
        result.warnings.append("network preflight passed")

    if not skip_camera:
        camera_type = get_camera_type()
        if camera_type == "PICAMERA":
            camera_ok, camera_message = check_picamera_available()
        else:
            camera_ok, camera_message = check_gopro_reachable()
        if camera_ok:
            result.warnings.append(f"camera preflight passed: {camera_message}")
        else:
            result.add_error(f"camera preflight failed: {camera_message}")

    if not skip_s3:
        try:
            bucket, access_key, secret_key = get_aws_credentials()
            region = get_aws_region()
            if bucket and access_key and secret_key:
                s3_ok, s3_message = check_s3_credentials(bucket, access_key, secret_key, region)
                if s3_ok:
                    result.warnings.append(f"S3 preflight passed: {s3_message}")
                else:
                    result.add_error(s3_message)
            else:
                result.add_error("S3 preflight skipped: incomplete AWS credentials")
        except RuntimeError as exc:
            result.add_error(str(exc))

    return result
