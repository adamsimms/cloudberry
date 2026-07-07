# Cloudberry

Raspberry Pi field rig for [Pinchard's Island](https://www.pinchards.is) — captures photos from a **GoPro HERO3/HERO4** or **Pi camera module**, uploads to S3, and powers down. Designed for WittyPi boot-once deployments.

[![CI](https://github.com/adamsimms/cloudberry/actions/workflows/ci.yml/badge.svg)](https://github.com/adamsimms/cloudberry/actions/workflows/ci.yml)

## Artist Statement

The simplicity of the Cloudberry photographs belies the complexity of the solar-powered camera system that makes them possible. A camera affixed to Adam’s family’s cabin on Pinchard’s Island takes the photographs continuously throughout the day and uploads them to the internet via cellular network. Able to control the camera and access the images from anywhere, Adam uses technology to maintain a constant presence in a place that is inaccessible most of the year. In capturing a view that recalls the experience of looking out the cabin’s window, the camera stands in for the photographer. Thus, these photographs constitute a political act: they allow an uninterrupted foothold on a place that was effectively erased when the Canadian government resettled the area shortly after Newfoundland became the country’s 10th province.

Comprised of thousands of photographs, the enormity of the Cloudberry project has inspired Adam to explore a new aspect of the sublime in his work. While other projects have focused on the pursuit of a single majestic photograph, Cloudberry inspires awe through its abundance of quotidian images. The title itself parallels this shift: while it may at first evoke the vast Newfoundland sky, Cloudberry in fact references the indigenous wild berry—colloquially known as a “bakeapple”—that flourishes on the seemingly inhospitable land.

The Cloudberry photographs are at once static and dynamic: though the frame remains exactly the same, the landscape is constantly changing. The enormous variety in the images recalls series of Impressionist paintings that show the same scene in different types of light, in all seasons, and throughout the day. The sky, the ocean, and the terrain in the photographs seem to change more readily than the immutable rocks, but even their appearance eventually transforms as the seasons change. Though Cloudberry highlights the specificity of this particular landscape, it also manifests the familiar desire to connect to one’s homeland not as a relic of the past but as a place that is alive.


## Boot-once workflow

1. WittyPi powers the Pi on at the scheduled time
2. `scripts/systemd/cloudberry.service` runs `cloudberry` once at boot
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

Island Wi‑Fi and GoPro field notes are in [docs/field/secrets-reference.md](docs/field/secrets-reference.md) but are **not** loaded by the app.

## Configuration (`config.ini`)

| Key | Description |
|-----|-------------|
| `general.camera_type` | `H3`, `H4`, or `picamera` |
| `general.take_photo` | GoPro: shoot before downloading (`true`/`false`) |
| `general.delay` | Minutes to wait before capture |
| `general.shutdown_after` | Halt Pi after success |
| `gopro.ip` | GoPro IP (default `10.5.5.9`) |

See `config.ini.example` for Pi camera settings (`awb_mode`, `exposure_mode`, `meter_mode`, `iso`, and image tuning).

## CLI

```bash
cloudberry --check-config
cloudberry --dry-run
cloudberry --retry-failed
cloudberry --shutdown
```

## Field deployment

| Step | Resource |
|------|----------|
| Install Python deps + optional systemd | `./setup.sh` |
| WittyPi + optional shutdown sudoers | `./scripts/wittypi-setup.sh` |
| Boot-once schedule | Copy a `.wpi` from [scripts/wittypi/](scripts/wittypi/) into WittyPi |
| Systemd service | `scripts/systemd/cloudberry.service` (installed by `setup.sh`) |
| GoPro CSI firmware | `firmware/` |
| Hardware PDFs and setup logs | [docs/field/](docs/field/) |

## Repo layout

| Path | Purpose |
|------|---------|
| `cloudberry/` | Python package (CLI, GoPro, Pi camera, S3) |
| `docs/` | Contributor docs, IAM policy, field guides |
| `firmware/` | GoPro HERO4 official + CamDo CSI firmware |
| `scripts/wittypi/` | WittyPi schedule scripts (`.wpi`) |
| `scripts/wittypi-setup.sh` | WittyPi installer + optional shutdown sudoers |
| `scripts/systemd/` | Boot-once user service template |
| `assets/audio/` | Static audio assets |

## Contributing

We welcome bug fixes, docs improvements, and rig-hardening changes. Start with [CONTRIBUTING.md](CONTRIBUTING.md), then open a PR against `master`.

| Document | Purpose |
|----------|---------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Dev setup, checks, PR expectations |
| [SECURITY.md](SECURITY.md) | Vulnerability reporting |
| [CHANGELOG.md](CHANGELOG.md) | Release history |

```bash
pip install -e ".[dev]"
python3 -m ruff check .
python3 -m pytest
pre-commit run --all-files
```

On a Pi: `pip install -e ".[pi]"`.

## License

MIT — see [LICENSE](LICENSE).

Security: see [SECURITY.md](SECURITY.md)
