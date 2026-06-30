# Field secrets reference (not loaded by Cloudberry)

These values were used during island field setup. **Cloudberry v3** only reads the keys in [`.env.example`](../../.env.example) via `secrets.env`.

Keep this file for migration and hardware reference — do not commit live credentials.

## Island Wi‑Fi (`wpa_supplicant`)

| Network | Notes |
|---------|--------|
| `shutterisland` | GoPro HERO4 AP SSID (see `scripts/wittypi/shutterisland.wpi`) |
| `CamDoBlink_*` | CamDo Blink controller AP |

## GoPro

| Variable | Purpose |
|----------|---------|
| `GOPRO_WIFI_PASSWORD` | GoPro AP password — **required** in `secrets.env` for H3/H4 |
| `GOPRO_AP_PASSWORD` | Legacy alias; not read by v3 code |
| `GOPRO_MAC_ADDRESS` | Wake-on-LAN target for H4 |

## Remote access (historical)

| Service | Notes |
|---------|--------|
| Dataplicity | Remote shell; install token was one-time |
| Huawei E8372 LTE | Admin UI password on the modem |

## Camera Suite (pre-v3)

| Variable | Notes |
|----------|--------|
| `CAMERASUITE_EMAIL` | Registration email |
| `CAMERASUITE_SERIAL` | License serial |

Replaced by `picamera2` in v3 — see [camera_suite_raspberry_install.txt](camera_suite_raspberry_install.txt).

## SMTP alerts (removed)

v2 used `logging.ini` email handlers. v3 uses rotating file logs under `logs/` only.
