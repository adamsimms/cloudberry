"""GoPro HERO3/HERO4 control and media download."""

from __future__ import annotations

import logging
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

import xmltodict
from wakeonlan import send_magic_packet

from cloudberry.common import count_down
from cloudberry.config import get_bool_config, get_config
from cloudberry.secrets import gopro_mac_address, gopro_wifi_password

logger = logging.getLogger("Cloudberry")

DEFAULT_GOPRO_IP = "10.5.5.9"
URL_MEDIA = ":8080/videos/DCIM/"

H3_URLS = {
    "gopro_on": "/bacpac/PW?t={0}&p=%01",
    "gopro_off": "/bacpac/PW?t={0}&p=%00",
    "shutter_on": "/bacpac/SH?t={0}&p=%01",
    "shutter_off": "/bacpac/SH?t={0}&p=%00",
    "mode_photo": "/camera/CM?t={0}&p=%01",
    "delete_all": "/camera/DA?t={0}",
    "delete_last": "/camera/DL?t={0}",
    "set_date_time": "/camera/TM?t={0}&p=%",
}

H4_URLS = {
    "gopro_off": "/gp/gpControl/command/system/sleep",
    "shutter_on": "/gp/gpControl/command/shutter?p=1",
    "shutter_off": "/gp/gpControl/command/shutter?p=0",
    "mode_photo": "/gp/gpControl/command/mode?p=1",
    "delete": "/gp/gpControl/command/storage/delete?p=/100GOPRO/{file}",
    "delete_all": "/gp/gpControl/command/storage/delete/all",
}


def parse_media_page(content: bytes | str) -> list[dict]:
    if isinstance(content, bytes):
        content = content.decode("utf-8", errors="replace")
    data = xmltodict.parse(content)
    tr_list = data["html"]["body"]["div"]["div"]["table"]["tbody"]["tr"]
    if not isinstance(tr_list, list):
        tr_list = [tr_list]
    images = []
    for tr in tr_list:
        entry: dict = {}
        for td in tr["td"]:
            if "a" in td:
                link = td["a"]
                entry["name"] = link["#text"] if isinstance(link, dict) else str(link)
            elif "span" in td and not isinstance(td["span"], list):
                span = td["span"]
                text = span["#text"] if isinstance(span, dict) else str(span)
                entry["date"] = datetime.strptime(text, "%d-%b-%Y %H:%M")
        if entry.get("name") and (".JPG" in entry["name"] or ".MP4" in entry["name"]):
            images.append(entry)
    return sorted(images, key=lambda img: img["name"])


def gopro_base_url() -> str:
    ip = get_config("gopro", "ip", DEFAULT_GOPRO_IP)
    return f"http://{ip}"


class GoProCtrl:
    def __init__(self, camera_type: str):
        self.camera_type = camera_type.upper()
        self.password = gopro_wifi_password()
        self.urls = H3_URLS if self.camera_type == "H3" else H4_URLS

    def _command_url(self, path: str) -> str:
        if self.camera_type == "H3":
            return gopro_base_url() + path.format(self.password)
        return gopro_base_url() + path

    def send_cmd(self, path: str) -> bool:
        url = self._command_url(path)
        logger.debug("Sending command: %s", url)
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                result = response.read()
            logger.debug("Result from %s :: %s", url, result)
            return True
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            logger.error("Failed to send command to camera: %s", exc)
            return False

    def wake(self) -> bool:
        logger.info("Waking up the camera...")
        if self.camera_type == "H4":
            ip = get_config("gopro", "ip", DEFAULT_GOPRO_IP)
            return bool(
                send_magic_packet(
                    gopro_mac_address(),
                    ip_address=ip,
                    port=9,
                )
            )
        return self.send_cmd(self.urls["gopro_on"])

    def sleep(self) -> bool:
        logger.info("Putting the camera to sleep...")
        return self.send_cmd(self.urls["gopro_off"])

    def take_photo(self) -> bool:
        logger.info("Setting camera to photo mode...")
        if not self.send_cmd(self.urls["mode_photo"]):
            return False
        count_down(5)
        logger.info("Taking photo...")
        if not self.send_cmd(self.urls["shutter_on"]):
            return False
        count_down(5)
        return True

    def download(self, image_dir: Path, *, last: bool = False) -> list[tuple[Path, str | None]]:
        logger.info("Downloading photos from GoPro...")
        base = gopro_base_url()
        media_url = base + URL_MEDIA
        try:
            with urllib.request.urlopen(media_url, timeout=10) as response:
                result = response.read().decode("utf-8", errors="replace")
            folders = re.findall(r'href="(\d\d\dGOPRO)/"', result)
            if not folders:
                logger.error("No media folders found on GoPro")
                return []
            folder_url = f"{media_url}/{folders[-1]}"
            with urllib.request.urlopen(folder_url, timeout=10) as response:
                page = response.read()
            pics = parse_media_page(page)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            logger.error("GoPro download failed: %s", exc)
            return []

        if not pics:
            logger.error("No photos found on GoPro")
            return []

        selected = [max(pics, key=lambda item: item["name"])] if last else pics
        downloaded: list[tuple[Path, str | None]] = []
        for pic in selected:
            file_url = f"{folder_url}/{pic['name']}"
            with urllib.request.urlopen(file_url, timeout=30) as response:
                timestamp = pic.get("date", datetime.now()).isoformat()
                filename = f"{timestamp}.000Z_{pic['name']}"
                logger.info("Downloading %s...", filename)
                destination = image_dir / filename
                with destination.open("wb") as handle:
                    while True:
                        chunk = response.read(16 * 1024)
                        if not chunk:
                            break
                        handle.write(chunk)
                        sys.stdout.flush()
            downloaded.append((destination, pic["name"]))
        return downloaded

    def delete(self, file_name: str) -> bool:
        logger.info("Deleting %s from GoPro", file_name)
        if self.camera_type == "H3":
            return self.send_cmd(self.urls["delete_last"])
        return self.send_cmd(self.urls["delete"].format(file=file_name))


def capture_from_gopro(
    image_dir: Path, camera_type: str
) -> tuple[list[tuple[Path, str | None]], GoProCtrl]:
    gopro = GoProCtrl(camera_type)
    gopro.wake()
    count_down(10)

    if get_bool_config("general", "take_photo", default=False):
        gopro.take_photo()

    files = gopro.download(image_dir, last=False)
    logger.info("Downloaded %s file(s) from GoPro", len(files))
    count_down(5)
    return files, gopro
