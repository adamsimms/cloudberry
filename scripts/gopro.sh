#!/usr/bin/env bash
# Boot-once launcher — set CLOUDBERRY_DIR to your install path (default: /home/pi/cloudberry).
# Prefer systemd/cloudberry.service for new deployments; this script remains for network-up hooks.
set -euo pipefail
RIG_DIR="${CLOUDBERRY_DIR:-/home/pi/cloudberry}"
cd "${RIG_DIR}"
exec "${RIG_DIR}/.venv/bin/cloudberry"
