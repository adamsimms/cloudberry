"""Pi Camera capture for Cloudberry."""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger("Cloudberry")

AWB_MODES = {
    "auto": 0,
    "incandescent": 1,
    "tungsten": 2,
    "fluorescent": 3,
    "indoor": 4,
    "daylight": 5,
    "cloudy": 6,
    "custom": 7,
}

EXPOSURE_MODES = {
    "normal": 0,
    "short": 1,
    "long": 2,
    "custom": 3,
}

METER_MODES = {
    "centre": 0,
    "center": 0,
    "spot": 1,
    "matrix": 2,
    "average": 3,
}


def _parse_resolution(value: str) -> tuple[int, int]:
    width, height = value.lower().split("x", 1)
    return int(width), int(height)


def _parse_float(value: str, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _parse_int(value: str, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _map_control_value(value: str, mapping: dict[str, int]) -> int | None:
    normalized = value.strip().lower()
    if normalized.isdigit():
        return int(normalized)
    return mapping.get(normalized)


def build_picamera_controls(camera_settings: dict[str, str]) -> dict[str, float | int]:
    controls: dict[str, float | int] = {
        "Brightness": _parse_float(camera_settings.get("brightness", "0.0"), 0.0),
        "Contrast": _parse_float(camera_settings.get("contrast", "1.0"), 1.0),
        "Sharpness": _parse_float(camera_settings.get("sharpness", "1.0"), 1.0),
        "Saturation": _parse_float(camera_settings.get("saturation", "1.0"), 1.0),
        "AnalogueGain": _parse_float(camera_settings.get("analogue_gain", "1.0"), 1.0),
    }

    if awb_mode := camera_settings.get("awb_mode"):
        mapped = _map_control_value(awb_mode, AWB_MODES)
        if mapped is not None:
            controls["AwbMode"] = mapped

    if exposure_mode := camera_settings.get("exposure_mode"):
        mapped = _map_control_value(exposure_mode, EXPOSURE_MODES)
        if mapped is not None:
            controls["AeExposureMode"] = mapped

    if meter_mode := camera_settings.get("meter_mode"):
        mapped = _map_control_value(meter_mode, METER_MODES)
        if mapped is not None:
            controls["AeMeteringMode"] = mapped

    if iso := camera_settings.get("iso"):
        iso_value = _parse_int(iso, 0)
        if iso_value > 0:
            controls["Iso"] = iso_value

    return controls


def capture_photo(image_dir: Path, camera_settings: dict[str, str]) -> Path:
    try:
        from picamera2 import Picamera2
    except ImportError as exc:
        raise RuntimeError(
            "picamera2 is required for camera_type=picamera. "
            "Install with: pip install -e '.[pi]'"
        ) from exc

    resolution = camera_settings.get("resolution", "2592x1944")
    warmup_seconds = _parse_int(camera_settings.get("warmup_seconds", "2"), 2)
    jpeg_quality = _parse_int(camera_settings.get("jpeg_quality", "95"), 95)
    size = _parse_resolution(resolution)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%S")
    image_path = image_dir / f"{timestamp}.000Z_PiCamera.jpg"

    with Picamera2() as camera:
        config = camera.create_still_configuration(main={"size": size})
        camera.configure(config)
        camera.set_controls(build_picamera_controls(camera_settings))
        camera.options["quality"] = jpeg_quality
        camera.start()
        time.sleep(warmup_seconds)
        camera.capture_file(str(image_path))

    logger.info("Captured photo: %s", image_path)
    return image_path
