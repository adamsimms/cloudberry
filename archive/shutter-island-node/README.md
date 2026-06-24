# shutter-island (Node.js) — archived reference

Early Raspberry Pi + GoPro HERO4 automation from the private [shutter-island](https://github.com/adamsimms/shutter-island) repo (2017–2018).

**Canonical rig software is now the Python app in this repo's root** (`main.py`). These files are kept for historical reference only.

## Contents

| Path | Description |
|------|-------------|
| `cloudberry-js/` | Node.js scripts using `goproh4` (download, snapshot, power, settings) |
| `tests/hellogopro4/` | GoPro Wi‑Fi API experiments and settings |
| `tests/cloudpistill-snapshot.js` | Raspberry Pi camera (`node-raspistill`) test |
| `init.d/GoProDownload` | SysV init script example for cron-style download |
| `field-notes.txt` | Field debugging notes and reference links |

## Related repos

- **[cloudberry](https://github.com/adamsimms/cloudberry)** — this repo; Python controller with S3 upload
- **[pinchards.is](https://github.com/adamsimms/pinchards.is)** — gallery website at [www.pinchards.is](http://www.pinchards.is)
