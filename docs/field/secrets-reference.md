# Field secrets reference (not loaded by Cloudberry)

**Cloudberry v3** only reads the keys in [`.env.example`](../../.env.example) via `secrets.env`. This file documents island field-network context — do not commit live credentials.

## Island Wi‑Fi (`wpa_supplicant`)

| Network | Notes |
|---------|--------|
| `shutterisland` | GoPro HERO4 AP SSID (see `scripts/wittypi/shutterisland.wpi`) |
| `CamDoBlink_*` | CamDo Blink controller AP |

## GoPro

| Variable | Purpose |
|----------|---------|
| `GOPRO_WIFI_PASSWORD` | GoPro AP password — **required** in `secrets.env` for H3/H4 |
| `GOPRO_MAC_ADDRESS` | Wake-on-LAN target for H4 |
