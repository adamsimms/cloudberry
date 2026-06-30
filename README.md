# Cloudberry

Raspberry Pi field rig for [Pinchard's Island](http://www.pinchards.is) — captures photos from a **GoPro HERO3/HERO4** or **Pi camera module**, uploads to S3, and powers down. Designed for WittyPi boot-once deployments.

[![CI](https://github.com/adamsimms/cloudberry/actions/workflows/ci.yml/badge.svg)](https://github.com/adamsimms/cloudberry/actions/workflows/ci.yml)

> Supersedes the legacy [shutter-island](https://github.com/adamsimms/shutter-island) Node experiments and the deprecated **piberry** repo (Pi Camera-only fork). See `archive/shutter-island/` for 2017 rig history.

## Boot-once workflow

1. WittyPi powers the Pi on at the scheduled time
2. `cloudberry` runs once (systemd or `scripts/gopro.sh`)
3. Capture from GoPro or Pi camera, upload to S3
4. Optional `shutdown_after` halts the Pi until the next wake-up

## Camera modes

| `camera_type` | Hardware |
|---------------|----------|
| `H4` | GoPro HERO4 over Wi‑Fi (default for Pinchard's Island) |
| `H3` | GoPro HERO3 over Wi‑Fi |
| `picamera` | Official Raspberry Pi camera module (`picamera2`) |

## Quick start

```bash
git clone https://github.com/adamsimms/cloudberry.git
cd cloudberry
cp .env.example secrets.env
cp config.ini.example config.ini
chmod 600 secrets.env config.ini
# Edit secrets.env and config.ini

./setup.sh
cloudberry --check-config
cloudberry
```

## Secrets (`secrets.env`)

Never commit credentials. Copy `.env.example` → `secrets.env`:

- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET`
- `GOPRO_WIFI_PASSWORD` (required for H3/H4)
- `GOPRO_MAC_ADDRESS` (for H4 wake-on-LAN)

Also supported: `~/.cloudberry/secrets.env` or `CLOUDBERRY_SECRETS_FILE`.

## Configuration (`config.ini`)

| Key | Description |
|-----|-------------|
| `general.camera_type` | `H3`, `H4`, or `picamera` |
| `general.take_photo` | GoPro: shoot before downloading (`true`/`false`) |
| `general.delay` | Minutes to wait before capture |
| `general.shutdown_after` | Halt Pi after success |
| `gopro.ip` | GoPro IP (default `10.5.5.9`) |

See `config.ini.example` for Pi camera settings.

## CLI

```bash
cloudberry --check-config
cloudberry --dry-run
cloudberry --retry-failed
cloudberry --shutdown
```

## Repo layout

| Path | Purpose |
|------|---------|
| `cloudberry/` | Python package (CLI, GoPro, Pi camera, S3) |
| `docs/field/` | Field guides (WittyPi, INA219, watchdog, setup logs) |
| `firmware/` | GoPro HERO4 official + CamDo CSI firmware |
| `examples/wittypi/` | WittyPi schedule scripts (`.wpi`) |
| `scripts/` | `gopro.sh` auto-start, WittyPi setup helper |
| `archive/shutter-island/` | Legacy Node.js rig + field tests |
| `libraries/` | WittyPi installer, low-power library |
| `systemd/` | Boot-once user service |

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md). Security: [SECURITY.md](SECURITY.md) — **hello@adamsimms.xyz**.

```bash
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .
python -m pytest
```

On a Pi: `pip install -r requirements-pi.txt`.

## License

MIT — see [LICENSE](LICENSE).
