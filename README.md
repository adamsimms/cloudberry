# GoPro Camera Controller

Raspberry Pi software for Pinchard's Island — captures GoPro photos, uploads to S3, displayed at [www.pinchards.is](http://www.pinchards.is).

_Supports H3 and H4_

> **Note:** This repo supersedes the legacy private [shutter-island](https://github.com/adamsimms/shutter-island) Node.js experiments. Hardware docs, Witty Pi schedules, and archived Node scripts were merged from shutter-island in 2026. See `archive/shutter-island/` for rig code and field tests.

## Repo layout

| Path | Purpose |
|------|---------|
| `main.py`, `config.ini`, `utils/` | Python GoPro controller (run on the Pi) |
| `Firmware/` | GoPro HERO4 official + CamDo CSI firmware and `autoexec.csi` scripts |
| `Documentation/` | Field guides (Witty Pi, INA219, watchdog, setup log) |
| `examples/wittypi/` | Witty Pi 2 schedule scripts (`.wpi`), including `shutterisland.wpi` |
| `libraries/` | `installWittyPi.sh`, Low-Power library zip |
| `script/` | `gopro.sh` auto-start, ffmpeg install |
| `archive/shutter-island/` | Legacy Node.js rig code + field tests (2017 history) |

## Secrets (never commit)

AWS keys, GoPro Wi‑Fi password, and other credentials live in **`secrets.env`** (gitignored), not in `config.ini`.

1. Copy the template: `cp .env.example secrets.env`
2. Fill in values (keep a backup in your password manager)
3. On the Pi you can also use `~/.cloudberry/secrets.env`

`main.py` loads `secrets.env` automatically via `utils/secrets.py`. Required variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET`, `GOPRO_WIFI_PASSWORD`.

**If you ever had AWS keys in an old `config.ini`:** rotate them in IAM — purging git history does not invalidate exposed keys.

## Install dependencies

    cd cloudberry
    sudo pip install -r requirements.txt

## Execute script

Before executing, please make sure that the Raspberry Pi is connected to the GoPro Camera via wifi.

    python3 main.py

## Enable auto-starting

    sudo cp gopro.sh /etc/network/if-up.d/
    sudo chmod 755 /etc/network/if-up.d/gopro.sh

## GoPro
Navigate via USB: `gphoto2://[usb:001,012]/DCIM/100GOPRO`

GoPro4 Wifi Commands, with pairing instruction: 
    https://github.com/KonradIT/goprowifihack/blob/master/HERO4/WifiCommands.md

## WittyPi2

Install:

    wget http://www.uugear.com/repo/WittyPi2/installWittyPi.sh
    sudo sh installWittyPi.sh

Run:

    cd ~/wittyPi && sudo ./wittyPi.sh

Schedule examples (including the island capture schedule) are in `examples/wittypi/`. Copy a `.wpi` file to `~/wittyPi/schedule.wpi` and run `sudo ./runScript`, or select one when running `wittyPi.sh`. See `examples/wittypi/README` for format details.

## Real VNC

- https://www.realvnc.com/en/docs/raspberry-pi.html#raspberry-pi-setup
- https://www.realvnc.com/en/docs/raspberry-pi.html#raspberry-pi-connect-cloud
- https://www.raspberrypi.org/documentation/remote-access/vnc/

Start VNC:

    sudo systemctl stop vncserver-x11-serviced.service 
    sudo systemctl start vncserver-x11-serviced.service && vncserver

## CameraSuite

Install:

    sudo apt-get update
    sudo apt-get upgrade
  
    sudo apt-get install openssl sqlite libts-0.0 libinput5 libgles2-mesa libstdc++$
    libc6 libegl1-mesa libegl1-mesa-drivers libexpat1 libz1 libpng12-0 libevdev2 li$
    libxdmcp6 libxau6 libfreetype6 libfontconfig1 libmtdev1 libudev1 libxkbcommon0 $
    libx11-6 libx11-xcb1 libxext6 libts-0.0-0 libxcb1 libdbus-1.3

    sudo apt-get install gstreamer1.0-omx libgstreamer1.0-dev libgstreamer-plugins-base1.0

    mkdir ~/camerasuite && cd ~/camerasuite

    wget http://www.camerasuite.org/dl/camerasuitepi.tar.gz
    tar xfv camerasuitepi.tar.gz

Run:
    
    cd camerasuite && ./camerasuite.sh -platform xcb

## WiFi Scribbles

List wlan0 status:

    iwconfig

Scan available WiFi Networks:

    sudo iwlist wlan0 scan
    sudo wpa_cli

Wifi up and down:

    sudo ifconfig wlan0 up
    sudo ifconfig wlan0 down

Edit and reconfigure wpa_supplicant.conf:

    sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
    sudo wpa_cli -i wlan0 reconfigure

What's going on with wpa_supplicatant:
    
    sudo wpa_supplicant -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf -d
    ps aux | grep wpa_supplicant
