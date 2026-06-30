# Field hardware guides

Pinchard's Island rig reference material. Paths below are relative to this directory.

| File | Description |
|------|-------------|
| [WittyPi2_UserManual.pdf](WittyPi2_UserManual.pdf) | UUGear WittyPi 2 user manual (vendored; refreshed monthly by CI) |
| [ina219.pdf](ina219.pdf) | INA219 current sensor notes |
| [DualWatchDog_110216-V2.02.pdf](DualWatchDog_110216-V2.02.pdf) | SwitchDoc dual watchdog timer board |
| [arduino-mini-pro-to-isp.JPG](arduino-mini-pro-to-isp.JPG) | Arduino Pro Mini ISP wiring photo |
| [setup_command_log.redacted.txt](setup_command_log.redacted.txt) | Redacted field install log (2017 era) |
| [camera_suite_raspberry_install.txt](camera_suite_raspberry_install.txt) | **Legacy** Camera Suite install (pre-v3; v3 uses `picamera2`) |
| [secrets-reference.md](secrets-reference.md) | Historical field-network secrets (not loaded by app) |

## Related repo paths

- [examples/wittypi/](../../examples/wittypi/) — WittyPi schedule scripts (`.wpi`)
- [scripts/wittypi-setup.sh](../../scripts/wittypi-setup.sh) — WittyPi installer + optional shutdown sudoers
- [firmware/](../../firmware/) — GoPro HERO4 official and CamDo CSI firmware
- [systemd/cloudberry.service](../../systemd/cloudberry.service) — Boot-once systemd unit
