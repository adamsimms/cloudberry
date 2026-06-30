"""System shutdown helpers for boot-once WittyPi deployments."""

import logging
import subprocess


def shutdown_system(logger: logging.Logger | None = None) -> bool:
    """Request an immediate system halt. Requires passwordless sudo for shutdown."""
    log = logger or logging.getLogger("Cloudberry")
    log.info("Requesting system shutdown")
    try:
        result = subprocess.run(
            ["sudo", "shutdown", "-h", "now"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        log.error("Failed to run shutdown command: %s", exc)
        return False

    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown error"
        log.error("Shutdown command failed (%s): %s", result.returncode, stderr)
        return False

    return True
