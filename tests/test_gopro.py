from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from cloudberry.gopro import GoProCtrl, capture_from_gopro, parse_media_page


def test_parse_media_page_extracts_jpg_files():
    content = """<?xml version="1.0" encoding="UTF-8"?>
    <html><body><div><div><table><tbody><tr>
      <td><a>GOPR0001.JPG</a></td><td><span>01-Jan-2024 12:00</span></td>
    </tr><tr>
      <td><a>GOPR0002.JPG</a></td><td><span>02-Jan-2024 13:00</span></td>
    </tr></tbody></table></div></div></body></html>"""

    images = parse_media_page(content)

    assert len(images) == 2
    assert images[0]["name"] == "GOPR0001.JPG"
    assert images[1]["name"] == "GOPR0002.JPG"


def test_gopro_h4_wake_sends_magic_packet(monkeypatch):
    monkeypatch.setattr("cloudberry.gopro.gopro_wifi_password", lambda: "pw")
    monkeypatch.setattr("cloudberry.gopro.gopro_mac_address", lambda: "AA:BB:CC:DD:EE:FF")
    def fake_get_config(section, option, default=None):
        return "10.5.5.9"

    monkeypatch.setattr("cloudberry.gopro.get_config", fake_get_config)

    with patch("cloudberry.gopro.send_magic_packet", return_value=True) as mock_wake:
        ctrl = GoProCtrl("H4")
        assert ctrl.wake() is True
        mock_wake.assert_called_once()


def test_gopro_h3_wake_uses_command(monkeypatch):
    monkeypatch.setattr("cloudberry.gopro.gopro_wifi_password", lambda: "pw")

    with patch.object(GoProCtrl, "send_cmd", return_value=True) as mock_cmd:
        ctrl = GoProCtrl("H3")
        assert ctrl.wake() is True
        mock_cmd.assert_called_once()


def test_send_cmd_returns_false_on_error(monkeypatch):
    monkeypatch.setattr("cloudberry.gopro.gopro_wifi_password", lambda: "pw")

    with patch("urllib.request.urlopen", side_effect=OSError("fail")):
        ctrl = GoProCtrl("H4")
        assert ctrl.send_cmd("/test") is False


def test_delete_h4_formats_file_name(monkeypatch):
    monkeypatch.setattr("cloudberry.gopro.gopro_wifi_password", lambda: "pw")

    with patch.object(GoProCtrl, "send_cmd", return_value=True) as mock_cmd:
        ctrl = GoProCtrl("H4")
        assert ctrl.delete("GOPR0001.JPG") is True
        mock_cmd.assert_called_once()


def test_capture_from_gopro_skips_shoot_when_disabled(monkeypatch, tmp_path):
    monkeypatch.setattr("cloudberry.gopro.get_bool_config", lambda *args, **kwargs: False)
    monkeypatch.setattr("cloudberry.gopro.count_down", lambda seconds: None)

    gopro = MagicMock()
    gopro.wake.return_value = True
    gopro.download.return_value = [(tmp_path / "photo.jpg", "GOPR0001.JPG")]

    with patch("cloudberry.gopro.GoProCtrl", return_value=gopro):
        files, returned_gopro = capture_from_gopro(tmp_path, "H4")

    gopro.take_photo.assert_not_called()
    assert len(files) == 1
    assert returned_gopro is gopro


def test_download_fetches_media_from_gopro(monkeypatch, tmp_path):
    monkeypatch.setattr("cloudberry.gopro.gopro_wifi_password", lambda: "pw")
    monkeypatch.setattr(
        "cloudberry.gopro.get_config",
        lambda section, option, default=None: "10.5.5.9",
    )

    class FakeResponse:
        def __init__(self, payload: bytes):
            self._payload = payload

        def read(self, size: int = -1) -> bytes:
            if not self._payload:
                return b""
            if size < 0:
                data, self._payload = self._payload, b""
                return data
            data, self._payload = self._payload[:size], self._payload[size:]
            return data

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    responses = iter(
        [
            FakeResponse(b'<a href="100GOPRO/">100GOPRO</a>'),
            FakeResponse(b'<a href="GOPR0001.JPG">GOPR0001.JPG</a>'),
            FakeResponse(b"fake-jpeg"),
        ]
    )

    with patch("urllib.request.urlopen", side_effect=lambda *args, **kwargs: next(responses)):
        with patch(
            "cloudberry.gopro.parse_media_page",
            return_value=[
                {"name": "GOPR0001.JPG", "date": datetime(2024, 1, 1, tzinfo=timezone.utc)},
            ],
        ):
            ctrl = GoProCtrl("H4")
            downloaded = ctrl.download(tmp_path)

    assert len(downloaded) == 1
    assert downloaded[0][0].exists()
    assert downloaded[0][1] == "GOPR0001.JPG"
