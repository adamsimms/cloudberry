from unittest.mock import MagicMock

from cloudberry.cli import EXIT_CONFIG, EXIT_OK, main


def _ok_result():
    return type("Result", (), {"ok": True, "errors": [], "warnings": []})()


def test_check_config_reports_placeholder_errors(monkeypatch, tmp_path):
    monkeypatch.setattr("cloudberry.cli.ensure_config", lambda: tmp_path / "config.ini")
    monkeypatch.setattr(
        "cloudberry.cli.validate_config",
        lambda: type(
            "Result",
            (),
            {"ok": False, "errors": ["aws.bucket is missing"], "warnings": []},
        )(),
    )
    monkeypatch.setattr("cloudberry.cli.run_preflight_checks", lambda **kwargs: _ok_result())
    monkeypatch.setattr("cloudberry.cli.setup_logging", lambda **kwargs: MagicMock())

    exit_code = main(["--check-config"])
    assert exit_code == EXIT_CONFIG


def test_dry_run_skips_uploads(monkeypatch, tmp_path):
    monkeypatch.setattr("cloudberry.cli.IMAGE_DIR", tmp_path)
    monkeypatch.setattr("cloudberry.cli.ensure_config", lambda: tmp_path / "config.ini")
    monkeypatch.setattr("cloudberry.cli.validate_config", _ok_result)
    monkeypatch.setattr("cloudberry.cli.run_preflight_checks", lambda **kwargs: _ok_result())
    monkeypatch.setattr("cloudberry.cli.setup_logging", lambda **kwargs: MagicMock())

    def fake_get_config(*args, **kwargs):
        return kwargs.get("default") if "default" in kwargs else "0"

    monkeypatch.setattr("cloudberry.cli.get_config", fake_get_config)
    monkeypatch.setattr("cloudberry.cli.get_aws_credentials", lambda: ("bucket", "key", "secret"))
    monkeypatch.setattr("cloudberry.cli.get_aws_region", lambda: "us-east-1")
    monkeypatch.setattr("cloudberry.cli.get_bool_config", lambda *args, **kwargs: False)
    monkeypatch.setattr("cloudberry.cli.get_serial", lambda: "serial")
    monkeypatch.setattr("cloudberry.cli.count_down", lambda seconds: None)
    monkeypatch.setattr("cloudberry.cli.collect_upload_candidates", lambda *args, **kwargs: [])

    def fake_capture(image_dir, settings):
        return tmp_path / "new.jpg"

    monkeypatch.setattr("cloudberry.cli.get_camera_type", lambda: "PICAMERA")
    monkeypatch.setattr("cloudberry.cli.capture_photo", fake_capture)

    exit_code = main(["--dry-run", "--delay", "0"])
    assert exit_code == EXIT_OK
