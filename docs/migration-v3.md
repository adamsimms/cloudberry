# Migrating to Cloudberry v3.0

Upgrade guide for field rigs running pre-v3.0 Cloudberry (or the deprecated **piberry** fork).

## Before you start

- Target hardware: Raspberry Pi with Python **3.9+**
- Back up your existing `config.ini` and any credentials
- Default island setting remains **`camera_type = H4`**

## 1. Secrets: `config.ini` → `secrets.env`

v3 loads AWS and GoPro credentials **only** from `secrets.env` (or env vars), not `config.ini`.

```bash
cd ~/cloudberry   # or your install path
cp .env.example secrets.env
chmod 600 secrets.env
```

Move these values from your old `config.ini` `[aws]` / `[gopro]` sections (or piberry equivalent):

| Old location | New `secrets.env` key |
|--------------|----------------------|
| AWS access key | `AWS_ACCESS_KEY_ID` |
| AWS secret | `AWS_SECRET_ACCESS_KEY` |
| S3 bucket | `AWS_S3_BUCKET` |
| GoPro Wi‑Fi password | `GOPRO_WIFI_PASSWORD` |
| GoPro MAC (H4 WOL) | `GOPRO_MAC_ADDRESS` |

Non-secret settings stay in `config.ini`:

```bash
cp config.ini.example config.ini
# Restore general.* and gopro.ip from your backup; do not put secrets here
chmod 600 config.ini
```

## 2. Entry point: `python main.py` → `cloudberry`

| v2 / pre-v3 | v3 |
|-------------|-----|
| `python main.py` | `cloudberry` |
| `python main.py --check-config` | `cloudberry --check-config` |

Install the CLI:

```bash
./setup.sh
# or: pip install -e ".[pi]" inside your venv
```

Verify:

```bash
cloudberry --check-config
cloudberry --dry-run --delay 0
```

## 3. Boot path: `scripts/gopro.sh` → systemd

v3 removes the network-up shell hook. Use the **systemd user service** instead.

`./setup.sh` can install it interactively, or manually:

```bash
mkdir -p ~/.config/systemd/user
sed "s|%h|$HOME|g" systemd/cloudberry.service > ~/.config/systemd/user/cloudberry.service
systemctl --user daemon-reload
systemctl --user enable cloudberry.service
```

Remove old autostart hooks if present:

```bash
# If you previously used gopro.sh from /etc/network/if-up.d/ or similar:
sudo rm -f /etc/network/if-up.d/gopro.sh   # adjust path if different
```

Enable lingering so the user service runs at boot without a login session:

```bash
sudo loginctl enable-linger "$USER"
```

## 4. WittyPi setup

Use the repo helper instead of a vendored installer copy:

```bash
./scripts/wittypi-setup.sh
```

This installs WittyPi from UUGear and optionally sets `shutdown_after = true` plus the sudoers rule in `docs/sudoers-cloudberry-shutdown`.

## 5. Directory layout

| Pre-v3 path | v3 path |
|-------------|---------|
| `Documentation/` | `docs/field/` |
| `Firmware/` | `firmware/` |
| `script/` | `scripts/` (WittyPi setup only) |
| `utils/`, `urls_H3.py`, `urls_H4.py` | Removed — logic in `cloudberry/` package |

## 6. Pi camera (piberry users)

Set in `config.ini`:

```ini
[general]
camera_type = picamera
```

Install picamera2 on the Pi:

```bash
pip install -e ".[pi]"
# or: sudo apt install -y python3-picamera2
```

## 7. Post-upgrade checklist

- [ ] `cloudberry --check-config` passes
- [ ] `cloudberry --dry-run --delay 0` completes without errors
- [ ] `systemctl --user status cloudberry.service` shows enabled
- [ ] WittyPi schedule still wakes the Pi on time
- [ ] One live capture uploads to S3
- [ ] `shutdown_after` halts the Pi (if enabled)

## Need help?

Open a [GitHub issue](https://github.com/adamsimms/cloudberry/issues) (not for security — see [SECURITY.md](../SECURITY.md)).
