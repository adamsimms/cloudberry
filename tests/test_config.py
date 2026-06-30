import configparser

import pytest

from cloudberry import config as config_module


@pytest.fixture
def config_paths(tmp_path, monkeypatch):
    example = tmp_path / "config.ini.example"
    example.write_text(
        """
[general]
delay = 3
s3_key_prefix = test-prefix
make_public = true
camera_type = picamera

[picamera]
resolution = 1920x1080
""".strip(),
        encoding="utf-8",
    )
    target = tmp_path / "config.ini"
    monkeypatch.setattr(config_module, "EXAMPLE_CONFIG", example)
    monkeypatch.setattr(config_module, "DEFAULT_CONFIG", target)
    monkeypatch.setenv("CLOUDBERRY_CONFIG", str(target))
    config_module._config = configparser.ConfigParser()
    return target, example


def test_ensure_config_copies_example(config_paths):
    target, example = config_paths
    assert not target.exists()

    created = config_module.ensure_config()

    assert created == target
    assert target.read_text(encoding="utf-8") == example.read_text(encoding="utf-8")


def test_get_config_reads_values(config_paths):
    config_module.ensure_config()

    assert config_module.get_config("general", "delay") == "3"
    assert config_module.get_bool_config("general", "make_public") is True
    assert config_module.get_config("missing", "value", "fallback") == "fallback"


def test_get_section_config(config_paths):
    config_module.ensure_config()

    section = config_module.get_section_config("picamera")
    assert section["resolution"] == "1920x1080"


def test_get_aws_credentials_from_environment(config_paths, monkeypatch):
    config_module.ensure_config()
    monkeypatch.setenv("AWS_S3_BUCKET", "env-bucket")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "env-key")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "env-secret")

    bucket, key, secret = config_module.get_aws_credentials()

    assert bucket == "env-bucket"
    assert key == "env-key"
    assert secret == "env-secret"


def test_normalize_camera_type():
    assert config_module.normalize_camera_type("h4") == "H4"
    assert config_module.normalize_camera_type("picamera") == "PICAMERA"

    with pytest.raises(ValueError):
        config_module.normalize_camera_type("invalid")
