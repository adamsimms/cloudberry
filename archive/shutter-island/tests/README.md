# Tests — island lab notebook

Each folder is a separate experiment from the shutter-island era. None of this runs without old Pi hardware and npm packages, but the code and photos are the fun history.

## cloudpistill/

**Pi Camera Module** via `node-raspistill` — could the island use the Pi's own camera instead of (or alongside) the GoPro?

- `snapshot.js` — take a still
- [`captures/`](cloudpistill/captures/) — actual outputs from the Pi cam, summer 2017, sorted by date

```bash
cd cloudpistill && npm install && node snapshot.js
```

## hellogopro4/

**GoPro HERO4 Wi‑Fi API** hacking. Vendored a fork of the `goproh4` control library in `lib/` and tried every command.

| Script | Tried |
|--------|-------|
| `basic.js` | Connect and say hello |
| `snapshot.js` | Shutter press |
| `download.js` | Pull last file to ShutterBox |
| `listmedia.js` | Browse DCIM over Wi‑Fi |
| `poweron.js` / `poweroff.js` | Wake/sleep |
| `cloudberry_settings.js` | Photo mode, resolution, protune — documents every `gpControl/setting/` URL |

## helloaws/

**S3 upload pipeline** — the missing link between the Pi and [pinchards.is](http://www.pinchards.is). Mostly commented-out pseudocode (`upload.js`); never shipped. The `cloudberry` CLI in the cloudberry repo eventually did this with boto3.

## hellowatchdog/

**Dual WatchDog timer board** (SwitchDoc) — Arduino sketch to pat the hardware watchdog so a frozen Pi gets power-cycled. See `docs/field/DualWatchDog_110216-V2.02.pdf` in the cloudberry repo.

## cron/

**`GoProDownload`** — SysV init script wired to run `rig/node/download.js` on boot. The "production" glue before Python took over.
