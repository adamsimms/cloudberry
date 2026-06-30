"""Pi Camera capture for Cloudberry."""

import logging
import time
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger("Cloudberry")


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


def capture_photo(image_dir: Path, camera_settings: dict[str, str]) -> Path:
    try:
        from picamera2 import Picamera2
    except ImportError as exc:
        raise RuntimeError(
            "picamera2 is required for camera_type=picamera. "
            "Install with: pip install -r requirements-pi.txt"
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
        camera.set_controls(
            {
                "Brightness": _parse_float(camera_settings.get("brightness", "0.0"), 0.0),
                "Contrast": _parse_float(camera_settings.get("contrast", "1.0"), 1.0),
                "Sharpness": _parse_float(camera_settings.get("sharpness", "1.0"), 1.0),
                "Saturation": _parse_float(camera_settings.get("saturation", "1.0"), 1.0),
                "AnalogueGain": _parse_float(camera_settings.get("analogue_gain", "1.0"), 1.0),
            }
        )
        camera.options["quality"] = jpeg_quality
        camera.start()
        time.sleep(warmup_seconds)
        camera.capture_file(str(image_path))

    logger.info("Captured photo: %s", image_path)
    return image_path
