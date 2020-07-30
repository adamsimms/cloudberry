cd ~/ShutterIsland/repo/shutter-island/cloudberry
cd ~/ShutterIsland/ShutterBox/ && aws s3 sync .  s3://shutter-island/

cd ~/wittyPi && sudo ./wittyPi.sh
cd camerasuite && ./camerasuite.sh -platform xcb

sudo systemctl stop vncserver-x11-serviced.service && sudo systemctl start vncserver-x11-serviced.service && vncserver

sudo iwlist wlan0 scan
iwconfig
sudo wpa_cli -i wlan0 reconfigure
sudo wpa_cli

sudo ifconfig wlan0 up
sudo ifconfig wlan0 down

sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

sudo wpa_supplicant -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf -d

ps aux | grep wpa_supplicant
