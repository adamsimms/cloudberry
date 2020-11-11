from settings import GOPRO_IP

url_media = ":8080/videos/DCIM/"


url_gopro_off = "/gp/gpControl/command/system/sleep"

url_shutter_on = "/gp/gpControl/command/shutter?p=1"
url_shutter_off = "/gp/gpControl/command/shutter?p=0"

url_video_mode = "/gp/gpControl/command/mode?p=0"
url_mode_photo = "/gp/gpControl/command/mode?p=1"

url_photo_single = "/gp/gpControl/command/sub_mode?mode=1&sub_mode=0"
url_photo_night = "/gp/gpControl/command/sub_mode?mode=1&sub_mode=2"

url_photo_res_12MP_wide = "/gp/gpControl/setting/17/0"
url_photo_res_7MP_wide = "/gp/gpControl/setting/17/1"
url_photo_res_7MP_med = "/gp/gpControl/setting/17/2"
url_photo_res_5MP_med = "/gp/gpControl/setting/17/3"

url_default_photo = "/gp/gpControl/setting/53/1"

url_delete_last = "/gp/gpControl/command/storage/delete/last"
url_delete_all = "/gp/gpControl/command/storage/delete/all"

url_filelist = "/gp/gpMediaList"
url_filepath = "http://{}:8080/videos/DCIM/100GOPRO/".format(GOPRO_IP)
