# Cabinberry card logs (2017-11 to 2019-12)

Scrubbed extracts from the original Cloudberry Raspberry Pi SD card, cloned 2026-09-18. Hostname on the card: `cabinberry`. Witty Pi 2.56.

These files are **evidence**, not current runtime config. Do not copy them over `scripts/wittypi/shutterisland.wpi` or into `config.ini`.

## In this folder

| File | Source on the card |
|------|-------------------|
| [cloudberry.wpi](cloudberry.wpi) | `/home/pi/wittyPi/schedules/cloudberry.wpi` (mtime 2017-11-14). Artist: this was the only schedule in effect. 15 minutes on each hour 08:00-20:15, then off until 08:00. Other `.wpi` files in that folder were UUGear samples. |
| [schedule.log](schedule.log) | `/home/pi/wittyPi/schedule.log` |
| [wittyPi.log](wittyPi.log) | `/home/pi/wittyPi/wittyPi.log` |
| [gopro.log](gopro.log) | `/home/pi/gopro.log` |

## What we dropped

- The 2026-09-18 graphical boot (about 08:27-08:32 local).
- `config.ini` (AWS keys, GoPro password).
- `/var/log/syslog` (MAC addresses; also mixed in the 2026 boot).
- `.ssh`, leftover JPEGs, the 16 GB disk image.

A 2019-12-23 studio session remains in the logs and is not the 2017-18 field run.

## What the logs support

The Pi kept its hourly wake through the public catalog's 33-day silence (14 Nov-16 Dec 2017). From 1 Dec 2017 the GoPro path is mostly `HTTP 410 Gone` and `urlopen timed out`. That is a camera or camera-connection failure, not a dead Pi.

This card ran `camera_type H3`, `take_photo True`, bucket `shutter-island-test`. Local leftover names are `GOPR0380`-`GOPR0394`. That is not the public Hero4 series `GOPR1957`-`GOPR4132`. Do not cite these GOPR numbers as pinchards.is frames.

## Clone (not in git)

Desktop image `cloudberry-pi.img`, 15,931,539,456 bytes. SHA-256 `27fe6a3e2f625527593891095941a0edd13bbfde05209e8156e331b909451483`.
