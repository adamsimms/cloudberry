# Contributing to Cloudberry

Thanks for your interest in contributing. Cloudberry is the Pinchard's Island field rig — GoPro and Pi camera capture with S3 upload. This guide should get you from clone to pull request quickly.

## Before you start

1. Read the [README](README.md) to understand the **boot-once** workflow (WittyPi / systemd).
2. Review the [Code of Conduct](CODE_OF_CONDUCT.md).
3. Check [open issues](https://github.com/adamsimms/cloudberry/issues) and [open PRs](https://github.com/adamsimms/cloudberry/pulls).
4. For large changes, open an issue first.

## Development setup

```bash
git clone https://github.com/adamsimms/cloudberry.git
cd cloudberry
cp .env.example secrets.env
cp config.ini.example config.ini
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .
pre-commit install
```

On a Raspberry Pi: `pip install -r requirements-pi.txt`.

## Running checks

```bash
python -m ruff check .
python -m pytest
cloudberry --check-config
```

## Project structure

```
cloudberry/          # Python package
  cli.py             # orchestration
  gopro.py           # HERO3/HERO4
  camera.py          # picamera2
  secrets.py         # secrets.env loading
docs/field/          # island hardware guides
firmware/            # GoPro CSI firmware
examples/wittypi/    # schedule scripts
archive/             # shutter-island history
```

## Pull requests

1. Fork and branch from `master`.
2. Ensure `ruff` and `pytest` pass.
3. Update `CHANGELOG.md` for user-visible changes.
4. Open a PR with what changed and how you tested it.

## Security

Do not open public issues for vulnerabilities. Email **hello@adamsimms.xyz** — see [SECURITY.md](SECURITY.md).

## Versioning

Version in `pyproject.toml` and `cloudberry/__init__.py` (e.g. `v3.0.0`).
