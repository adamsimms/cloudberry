import sys
from unittest.mock import MagicMock, patch

import pytest

from cloudberry.camera import AWB_MODES, build_picamera_controls, capture_photo


def test_build_picamera_controls_maps_named_modes():
    controls = build_picamera_controls(
        {
            "awb_mode": "daylight",
            "exposure_mode": "short",
            "meter_mode": "matrix",
            "iso": "200",
            "brightness": "0.1",
        }
    )

    assert controls["AwbMode"] == AWB_MODES["daylight"]
    assert controls["AeExposureMode"] == 1
    assert controls["AeMeteringMode"] == 2
    assert controls["Iso"] == 200
    assert controls["Brightness"] == 0.1


def test_build_picamera_controls_accepts_numeric_strings():
    controls = build_picamera_controls({"awb_mode": "5", "iso": "0"})

    assert controls["AwbMode"] == 5
    assert "Iso" not in controls


def test_capture_photo_applies_advanced_controls(tmp_path):
    fake_module = MagicMock()
    fake_camera = MagicMock()
    fake_module.Picamera2.return_value.__enter__.return_value = fake_camera

    with patch.dict(sys.modules, {"picamera2": fake_module}):
        capture_photo(
            tmp_path,
            {
                "resolution": "640x480",
                "warmup_seconds": "0",
                "awb_mode": "cloudy",
                "meter_mode": "spot",
            },
        )

    controls = fake_camera.set_controls.call_args[0][0]
    assert controls["AwbMode"] == AWB_MODES["cloudy"]
    assert controls["AeMeteringMode"] == 1


def test_capture_photo_requires_picamera2(tmp_path, monkeypatch):
    import builtins

    real_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "picamera2":
            raise ImportError("no picamera2")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(RuntimeError, match="picamera2 is required"):
        capture_photo(tmp_path, {})
