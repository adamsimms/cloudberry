#!/usr/bin/env bash
# Legacy network-up hook — update paths for your Pi install directory.
set -euo pipefail
RIG_DIR="${CLOUDBERRY_DIR:-/home/pi/cloudberry}"
cd "${RIG_DIR}"
exec "${RIG_DIR}/.venv/bin/cloudberry"
