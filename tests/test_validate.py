from unittest.mock import MagicMock, patch

from cloudberry.validate import (
    ValidationResult,
    check_network,
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
