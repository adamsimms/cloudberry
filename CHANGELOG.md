# Changelog

## 3.0.0

- Modernize rig controller to Python 3.9+, `boto3`, and `picamera2`
- Consolidate GoPro (H3/H4) and Pi Camera (`picamera`) into `cloudberry` package
- Add CLI (`cloudberry`), preflight checks, upload queue, rotating logs, shutdown hook
- Secrets via `secrets.env` only (see `.env.example`); config in `config.ini`
- Reorganize repo: `docs/field/`, `firmware/`, `scripts/`, `systemd/`
- Add tests, CI, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT
- Supersedes the deprecated **piberry** repo (Pi Camera-only fork)
- Post-modernization cleanup: docs index, trimmed secrets example, CI matrix, expanded tests, fixed WittyPi workflow path

## Prior history

See git history before v3.0.0 for GoPro island rig development, shutter-island merge, and field documentation.
