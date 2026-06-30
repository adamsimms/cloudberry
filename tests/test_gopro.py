from unittest.mock import MagicMock, patch

from cloudberry.gopro import GoProCtrl, capture_from_gopro


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
