# GoPro Camera Controller
_Supports H3 and H4_

## Install dependencies

    cd cloudberry
    sudo pip install -r requirements.txt

## Execute script

Before executing, please make sure that the Raspberry Pi is connected to the GoPro Camera via wifi.

    python3 main.py

## Enable auto-starting

    sudo cp gopro.sh /etc/network/if-up.d/
    sudo chmod 755 /etc/network/if-up.d/gopro.sh
