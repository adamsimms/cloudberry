from unittest.mock import MagicMock, patch

from cloudberry.validate import (
    ValidationResult,
    check_gopro_reachable,
    check_network,
    run_preflight_checks,
    validate_config,
    validate_resolution,
)


def test_validate_resolution():
    assert validate_resolution("1920x1080")
    assert not validate_resolution("bad")


def test_validate_config_flags_missing_secrets(monkeypatch):
    monkeypatch.setattr("cloudberry.validate.get_aws_credentials", lambda: ("", "", ""))
    monkeypatch.setattr("cloudberry.validate.get_camera_type", lambda: "H4")
    monkeypatch.setattr(
        "cloudberry.validate.gopro_wifi_password",
        lambda: (_ for _ in ()).throw(RuntimeError("missing")),
    )
    monkeypatch.setattr("cloudberry.validate.load_secrets", lambda: None)

    result = validate_config()

    assert not result.ok
    assert any("AWS credentials" in error for error in result.errors)
    assert any("GOPRO_WIFI_PASSWORD" in error for error in result.errors)


def test_check_network_success():
    with patch("socket.create_connection", return_value=MagicMock()):
        assert check_network() is True


def test_check_network_failure():
    with patch("socket.create_connection", side_effect=OSError("offline")):
        assert check_network() is False


def test_validation_result_ok():
    result = ValidationResult()
    assert result.ok

    result.add_error("problem")
    assert not result.ok


def test_run_preflight_checks_collects_errors(monkeypatch):
    monkeypatch.setattr("cloudberry.validate.check_network", lambda: False)
    monkeypatch.setattr("cloudberry.validate.get_camera_type", lambda: "H4")
    monkeypatch.setattr(
        "cloudberry.validate.check_gopro_reachable",
        lambda: (False, "GoPro offline"),
    )
    monkeypatch.setattr("cloudberry.validate.get_aws_credentials", lambda: ("b", "k", "s"))
    monkeypatch.setattr("cloudberry.validate.get_aws_region", lambda: "us-east-1")
    monkeypatch.setattr(
        "cloudberry.validate.check_s3_credentials",
        lambda *args: (True, "ok"),
    )

    result = run_preflight_checks()

    assert not result.ok
    assert any("network" in error for error in result.errors)
    assert any("GoPro offline" in error for error in result.errors)


def test_check_gopro_reachable_success(monkeypatch):
    monkeypatch.setattr(
        "cloudberry.validate.get_config",
        lambda section, option, default=None: "10.5.5.9",
    )

    with patch("socket.create_connection", return_value=MagicMock()):
        ok, message = check_gopro_reachable()

    assert ok
    assert "10.5.5.9" in message
