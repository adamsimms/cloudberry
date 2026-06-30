import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from cloudberry.camera import _parse_resolution, capture_photo


def test_parse_resolution():
    assert _parse_resolution("2592x1944") == (2592, 1944)


def test_capture_photo_uses_picamera2(tmp_path: Path):
    fake_module = MagicMock()
    fake_camera = MagicMock()
    fake_module.Picamera2.return_value.__enter__.return_value = fake_camera

    with patch.dict(sys.modules, {"picamera2": fake_module}):
        image_path = capture_photo(
            tmp_path,
            {
                "resolution": "640x480",
                "warmup_seconds": "0",
                "brightness": "0.1",
            },
        )

    assert image_path.parent == tmp_path
    assert image_path.name.endswith("_PiCamera.jpg")
    fake_camera.capture_file.assert_called_once()


def test_capture_photo_requires_picamera2(tmp_path: Path, monkeypatch):
    import builtins

    real_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "picamera2":
            raise ImportError("no picamera2")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(RuntimeError, match="picamera2 is required"):
        capture_photo(tmp_path, {})
