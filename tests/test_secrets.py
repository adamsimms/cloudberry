import os

from cloudberry import secrets


def test_load_secrets_file_sets_env(tmp_path, monkeypatch):
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    secrets_file = tmp_path / "secrets.env"
    secrets_file.write_text("AWS_ACCESS_KEY_ID=file-key\n", encoding="utf-8")

    secrets._load_secrets_file(secrets_file)

    assert os.environ["AWS_ACCESS_KEY_ID"] == "file-key"


def test_load_secrets_file_skips_comments_and_blanks(tmp_path, monkeypatch):
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    secrets_file = tmp_path / "secrets.env"
    secrets_file.write_text(
        "# comment\n\nAWS_ACCESS_KEY_ID=file-key\n",
        encoding="utf-8",
    )

    secrets._load_secrets_file(secrets_file)

    assert os.environ["AWS_ACCESS_KEY_ID"] == "file-key"


def test_load_secrets_does_not_override_existing_env(tmp_path, monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "env-key")
    secrets_file = tmp_path / "secrets.env"
    secrets_file.write_text("AWS_ACCESS_KEY_ID=file-key\n", encoding="utf-8")

    secrets._load_secrets_file(secrets_file)

    assert os.environ["AWS_ACCESS_KEY_ID"] == "env-key"


def test_load_secrets_uses_explicit_file(tmp_path, monkeypatch):
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    custom = tmp_path / "custom.env"
    custom.write_text("AWS_ACCESS_KEY_ID=custom-key\n", encoding="utf-8")
    monkeypatch.setenv("CLOUDBERRY_SECRETS_FILE", str(custom))

    secrets.load_secrets()

    assert os.environ["AWS_ACCESS_KEY_ID"] == "custom-key"


def test_aws_credentials(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "key")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "secret")
    monkeypatch.setenv("AWS_S3_BUCKET", "bucket")

    assert secrets.aws_credentials() == ("key", "secret", "bucket")


def test_gopro_wifi_password_required(monkeypatch):
    monkeypatch.delenv("GOPRO_WIFI_PASSWORD", raising=False)

    try:
        secrets.gopro_wifi_password()
    except RuntimeError as exc:
        assert "GOPRO_WIFI_PASSWORD" in str(exc)
    else:
        raise AssertionError("expected RuntimeError")


def test_gopro_mac_address_default(monkeypatch):
    monkeypatch.delenv("GOPRO_MAC_ADDRESS", raising=False)
    monkeypatch.setattr(secrets, "load_secrets", lambda: None)

    assert secrets.gopro_mac_address() == "AA:BB:CC:DD:EE:FF"
