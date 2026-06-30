from unittest.mock import MagicMock, patch

from cloudberry.shutdown import shutdown_system


def test_shutdown_system_success():
    logger = MagicMock()
    with patch("cloudberry.shutdown.subprocess.run") as run:
        run.return_value = MagicMock(returncode=0)
        assert shutdown_system(logger) is True
    run.assert_called_once()


def test_shutdown_system_failure():
    logger = MagicMock()
    with patch("cloudberry.shutdown.subprocess.run") as run:
        run.return_value = MagicMock(returncode=1, stderr="permission denied")
        assert shutdown_system(logger) is False
    logger.error.assert_called_once()
