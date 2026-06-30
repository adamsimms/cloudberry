from pathlib import Path
from unittest.mock import MagicMock, patch

from cloudberry.cli import (
    EXIT_CONFIG,
    EXIT_OK,
    EXIT_PREFLIGHT,
    EXIT_UPLOAD,
    main,
    shutdown_system,
    upload_file,
)


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


def test_upload_file_dry_run(tmp_path):
    logger = MagicMock()
    image_path = tmp_path / "photo.jpg"
    image_path.write_text("data", encoding="utf-8")
    failed_dir = tmp_path / "failed"
    queue_file = tmp_path / "queue.json"

    uploaded = upload_file(
        logger,
        image_path=image_path,
        dry_run=True,
        s3_client=None,
        bucket="bucket",
        key_prefix="pi-1",
        make_public=False,
        failed_dir=failed_dir,
        queue_file=queue_file,
        queued_paths=[],
    )

    assert uploaded is True
    assert image_path.exists()


def test_upload_file_failure_queues_failed_image(tmp_path, monkeypatch):
    logger = MagicMock()
    image_path = tmp_path / "photo.jpg"
    image_path.write_text("data", encoding="utf-8")
    failed_dir = tmp_path / "failed"
    failed_dir.mkdir()
    queue_file = tmp_path / "queue.json"
    queued_paths: list[Path] = []

    monkeypatch.setattr("cloudberry.cli.push_picture_to_s3", lambda *args, **kwargs: False)
    monkeypatch.setattr(
        "cloudberry.cli.mark_failed",
        lambda path, directory: directory / path.name,
    )
    monkeypatch.setattr("cloudberry.cli.save_queue", lambda queue, paths: None)

    uploaded = upload_file(
        logger,
        image_path=image_path,
        dry_run=False,
        s3_client=MagicMock(),
        bucket="bucket",
        key_prefix="pi-1",
        make_public=False,
        failed_dir=failed_dir,
        queue_file=queue_file,
        queued_paths=queued_paths,
    )

    assert uploaded is False
    assert queued_paths == [failed_dir / "photo.jpg"]


def test_main_returns_preflight_exit_code(monkeypatch, tmp_path):
    monkeypatch.setattr("cloudberry.cli.IMAGE_DIR", tmp_path)
    monkeypatch.setattr("cloudberry.cli.ensure_config", lambda: tmp_path / "config.ini")
    monkeypatch.setattr("cloudberry.cli.validate_config", _ok_result)
    monkeypatch.setattr("cloudberry.cli.setup_logging", lambda **kwargs: MagicMock())
    monkeypatch.setattr("cloudberry.cli.get_config", lambda *args, **kwargs: "0")
    monkeypatch.setattr("cloudberry.cli.get_bool_config", lambda *args, **kwargs: False)

    failed = type(
        "Result",
        (),
        {"ok": False, "errors": ["camera offline"], "warnings": []},
    )()
    monkeypatch.setattr("cloudberry.cli.run_preflight_checks", lambda **kwargs: failed)

    assert main(["--delay", "0"]) == EXIT_PREFLIGHT


def test_main_shutdown_after_success(monkeypatch, tmp_path):
    monkeypatch.setattr("cloudberry.cli.IMAGE_DIR", tmp_path)
    monkeypatch.setattr("cloudberry.cli.ensure_config", lambda: tmp_path / "config.ini")
    monkeypatch.setattr("cloudberry.cli.validate_config", _ok_result)
    monkeypatch.setattr("cloudberry.cli.run_preflight_checks", lambda **kwargs: _ok_result())
    monkeypatch.setattr("cloudberry.cli.setup_logging", lambda **kwargs: MagicMock())
    monkeypatch.setattr("cloudberry.cli.get_config", lambda *args, **kwargs: "0")
    monkeypatch.setattr("cloudberry.cli.get_aws_credentials", lambda: ("bucket", "key", "secret"))
    monkeypatch.setattr("cloudberry.cli.get_aws_region", lambda: "us-east-1")
    monkeypatch.setattr("cloudberry.cli.get_bool_config", lambda *args, **kwargs: False)
    monkeypatch.setattr("cloudberry.cli.get_serial", lambda: "serial")
    monkeypatch.setattr("cloudberry.cli.count_down", lambda seconds: None)
    monkeypatch.setattr("cloudberry.cli.collect_upload_candidates", lambda *args, **kwargs: [])
    monkeypatch.setattr("cloudberry.cli.get_camera_type", lambda: "PICAMERA")
    monkeypatch.setattr(
        "cloudberry.cli.capture_photo",
        lambda image_dir, settings: tmp_path / "photo.jpg",
    )
    monkeypatch.setattr("cloudberry.cli.create_s3_client", lambda *args: MagicMock())
    monkeypatch.setattr("cloudberry.cli.push_picture_to_s3", lambda *args, **kwargs: True)

    with patch("cloudberry.cli.shutdown_system", return_value=True) as shutdown:
        exit_code = main(["--shutdown", "--delay", "0"])

    assert exit_code == EXIT_OK
    shutdown.assert_called_once()


def test_main_reports_upload_failures(monkeypatch, tmp_path):
    monkeypatch.setattr("cloudberry.cli.IMAGE_DIR", tmp_path)
    monkeypatch.setattr("cloudberry.cli.ensure_config", lambda: tmp_path / "config.ini")
    monkeypatch.setattr("cloudberry.cli.validate_config", _ok_result)
    monkeypatch.setattr("cloudberry.cli.run_preflight_checks", lambda **kwargs: _ok_result())
    monkeypatch.setattr("cloudberry.cli.setup_logging", lambda **kwargs: MagicMock())
    monkeypatch.setattr("cloudberry.cli.get_config", lambda *args, **kwargs: "0")
    monkeypatch.setattr("cloudberry.cli.get_aws_credentials", lambda: ("bucket", "key", "secret"))
    monkeypatch.setattr("cloudberry.cli.get_aws_region", lambda: "us-east-1")
    monkeypatch.setattr("cloudberry.cli.get_bool_config", lambda *args, **kwargs: False)
    monkeypatch.setattr("cloudberry.cli.get_serial", lambda: "serial")
    monkeypatch.setattr("cloudberry.cli.count_down", lambda seconds: None)
    monkeypatch.setattr(
        "cloudberry.cli.collect_upload_candidates",
        lambda *args, **kwargs: [tmp_path / "pending.jpg"],
    )
    monkeypatch.setattr("cloudberry.cli.get_camera_type", lambda: "PICAMERA")
    monkeypatch.setattr(
        "cloudberry.cli.capture_photo",
        lambda *args, **kwargs: tmp_path / "new.jpg",
    )
    monkeypatch.setattr("cloudberry.cli.create_s3_client", lambda *args: MagicMock())
    monkeypatch.setattr("cloudberry.cli.push_picture_to_s3", lambda *args, **kwargs: False)
    monkeypatch.setattr(
        "cloudberry.cli.mark_failed",
        lambda path, directory: directory / path.name,
    )
    monkeypatch.setattr("cloudberry.cli.save_queue", lambda *args, **kwargs: None)

    (tmp_path / "pending.jpg").write_text("data", encoding="utf-8")
    (tmp_path / "failed").mkdir(exist_ok=True)

    assert main(["--delay", "0", "--no-capture"]) == EXIT_UPLOAD


def test_shutdown_system_success():
    logger = MagicMock()
    with patch("cloudberry.cli.subprocess.run") as run:
        run.return_value = MagicMock(returncode=0)
        assert shutdown_system(logger) is True
    run.assert_called_once()


def test_shutdown_system_failure():
    logger = MagicMock()
    with patch("cloudberry.cli.subprocess.run") as run:
        run.return_value = MagicMock(returncode=1, stderr="permission denied")
        assert shutdown_system(logger) is False
    logger.error.assert_called_once()
