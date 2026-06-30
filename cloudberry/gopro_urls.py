"""GoPro URL paths for HERO3 and HERO4."""

H3 = {
    "gopro_on": "/bacpac/PW?t={0}&p=%01",
    "gopro_off": "/bacpac/PW?t={0}&p=%00",
    "shutter_on": "/bacpac/SH?t={0}&p=%01",
    "shutter_off": "/bacpac/SH?t={0}&p=%00",
    "mode_photo": "/camera/CM?t={0}&p=%01",
    "delete_all": "/camera/DA?t={0}",
    "delete_last": "/camera/DL?t={0}",
    "set_date_time": "/camera/TM?t={0}&p=%",
}

H4 = {
    "gopro_off": "/gp/gpControl/command/system/sleep",
    "shutter_on": "/gp/gpControl/command/shutter?p=1",
    "shutter_off": "/gp/gpControl/command/shutter?p=0",
    "mode_photo": "/gp/gpControl/command/mode?p=1",
    "delete": "/gp/gpControl/command/storage/delete?p=/100GOPRO/{file}",
    "delete_all": "/gp/gpControl/command/storage/delete/all",
}
