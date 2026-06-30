from cloudberry.logging_setup import resolve_log_dir, setup_logging


def test_resolve_log_dir_default(tmp_path, monkeypatch):
    monkeypatch.setattr("cloudberry.logging_setup.DEFAULT_LOG_DIR", tmp_path / "logs")
    log_dir = resolve_log_dir()
    assert log_dir == tmp_path / "logs"
    assert log_dir.exists()


def test_resolve_log_dir_configured(tmp_path):
    custom = tmp_path / "custom-logs"
    log_dir = resolve_log_dir(str(custom))
    assert log_dir == custom
    assert custom.exists()


def test_setup_logging_writes_file(tmp_path):
    logger = setup_logging(log_dir=tmp_path)
    logger.info("test message")
    for handler in logger.handlers:
        handler.flush()
    assert (tmp_path / "cloudberry.log").exists()
