# Changelog

All notable changes to this project are documented here.

## 3.0.0

### Modernization

- Modernize rig controller to Python 3.9+, `boto3`, and `picamera2`
- Consolidate GoPro (H3/H4) and Pi Camera (`picamera`) into `cloudberry` package
- Add CLI (`cloudberry`), preflight checks, upload queue, rotating logs, shutdown hook
- Secrets via `secrets.env` only (see `.env.example`); config in `config.ini`
- Reorganize repo: `docs/field/`, `firmware/`, `scripts/`
- Add tests, CI, CONTRIBUTING, SECURITY

### Cleanup and hardening

- Fix WittyPi manual refresh workflow path; add field docs index
- Trim `.env.example` to app-loaded secrets; document historical vars separately
- CI matrix (Python 3.9/3.11/3.12), pre-commit, pytest coverage
- Expanded tests for secrets, GoPro download, CLI upload/shutdown/preflight paths
- Wire picamera `awb_mode`, `exposure_mode`, `meter_mode`, and `iso` config keys
- Remove deprecated `main.py` shim and `scripts/gopro.sh` network hook (use systemd)
- Remove duplicate `libraries/installWittyPi.sh` (use `scripts/wittypi-setup.sh`)
- Consolidate dependency installs on `pip install -e ".[dev]"` / `".[pi]"`
