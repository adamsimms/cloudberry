# Contributing to Cloudberry

Thanks for your interest in contributing. Cloudberry is the Pinchard's Island field rig — GoPro and Pi camera capture with S3 upload for boot-once WittyPi deployments.

## Before you start

1. Read the [README](README.md) for the boot-once workflow and repo layout.
2. Review the [Code of Conduct](CODE_OF_CONDUCT.md).
3. Check [open issues](https://github.com/adamsimms/cloudberry/issues) and [open PRs](https://github.com/adamsimms/cloudberry/pulls).
4. For large or architectural changes, open an issue first.

## Development setup

Requires **Python 3.9+** (CI tests 3.9, 3.11, and 3.12).

```bash
git clone https://github.com/adamsimms/cloudberry.git
cd cloudberry
cp .env.example secrets.env
cp config.ini.example config.ini
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

Dependencies are defined in `pyproject.toml`. The `requirements*.txt` files are pointers only — use the editable install above.

On a Raspberry Pi with a camera module:

```bash
pip install -e ".[pi,dev]"
```

## Running checks

Run these before opening a PR:

```bash
python3 -m ruff check .
python3 -m pytest --cov=cloudberry --cov-report=term-missing
pre-commit run --all-files
```

Optional local validation (requires filled `secrets.env`):

```bash
cloudberry --check-config
cloudberry --dry-run --delay 0
```

## Testing without hardware

Most tests use mocks — you do not need a Pi, GoPro, or AWS account to develop:

| Area | Approach |
|------|----------|
| GoPro HTTP | Mock `urllib.request.urlopen` |
| Pi camera | Mock `picamera2` module |
| S3 | Mock `boto3` client |
| Preflight | Mock network/camera/S3 checks |

Add tests under `tests/` for any behavior you change. Prefer testing public functions and CLI exit codes over internal details.

## Project structure

```
cloudberry/          # Python package
  cli.py             # orchestration and CLI
  gopro.py           # HERO3/HERO4 Wi-Fi control
  camera.py          # picamera2 capture
  secrets.py         # secrets.env loading
  validate.py        # config and preflight checks
docs/
  field/             # island hardware guides (PDFs, setup logs)
  aws-iam-policy.json
firmware/            # GoPro CSI firmware
examples/wittypi/    # WittyPi schedule scripts
archive/             # shutter-island history (read-only)
systemd/             # boot-once user service template
```

## Pull requests

1. Fork and branch from `master`.
2. Keep changes focused — match existing style and naming.
3. Update `CHANGELOG.md` for user-visible changes.
4. Update `README.md` and `config.ini.example` if config or CLI behavior changes.
5. Ensure ruff, pytest, and pre-commit pass.
6. Open a PR using the template — describe what changed and how you tested it.

Do **not** commit `secrets.env`, `config.ini`, credentials, or field photos.

## Security

Do not open public issues for vulnerabilities. Use [GitHub private vulnerability reporting](https://github.com/adamsimms/cloudberry/security/advisories/new) — see [SECURITY.md](SECURITY.md).

## Versioning

- Version lives in `pyproject.toml` and `cloudberry/__init__.py`.
- Tag releases as `vX.Y.Z` on `master` after merge.
- Document breaking changes clearly in `CHANGELOG.md`.

## Questions

Open a GitHub issue for questions that are not security-sensitive.
