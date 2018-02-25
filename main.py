import glob
import os
import logging.config
import re
import time
import sys
import datetime
import settings
import urls_H3
import urls_H4
from utils.common import count_down
from utils.config_util import get_config
import urllib2
import boto
from boto.s3.key import Key
import socket

cur_dir = os.path.dirname(os.path.realpath(__file__)) + '/'

logging.config.fileConfig(os.path.join(cur_dir, 'logging.ini'))
logger = logging.getLogger('GoPro')


aws_bucket = get_config('aws', 'bucket')
aws_key = get_config('aws', 'KEY')
aws_security = get_config('aws', 'SECRET')


image_path = os.path.join(cur_dir, 'images')
if not os.path.exists(image_path):
    os.mkdir(image_path)

camera_type = get_config('general', 'camera_type', 'H3')

url_base = urls_H3 if camera_type == 'H3' else urls_H4


class GoProCtrl:

    def __init__(self):
        pass

    def wake(self):
        logger.info("Wake up GoPro...")
        if camera_type == "H4":
            return self.send_cmd(url_base.url_shutter_on)
        else:
            return self.send_cmd(url_base.url_gopro_on)

    @staticmethod
    def send_cmd(cmd):
        if camera_type == "H4":
            url = settings.GOPRO_URL + cmd
        else:
            url = settings.GOPRO_URL + cmd.format(get_config('gopro', 'password'))

        print("Sending command,   ", url)

        try:
            urllib2.urlopen(url, timeout=10).read()
            return True
        except Exception as e:
            logger.error('Failed to send command to GoPro: {}'.format(e))

    def sleep(self):
        logger.info("- Sleep")
        return self.send_cmd(url_base.url_gopro_off)

    def delete_all(self):
        logger.info("- Deleting all")
        return self.send_cmd(url_base.url_delete_all)

    def takepic(self):
        logger.info("- take a photo")
        if not self.send_cmd(url_base.url_mode_photo):
            return False
        count_down(5)  # wait for photo mode to turn on
        if not self.send_cmd(url_base.url_shutter_on):
            return False
        count_down(1)  # wait for photo to be taken
        return True

    def set_date_time(self):
        logger.info("setting date and time...")
        s = time.strftime("%y%%%m%%%d%%%H%%%M%%%S", time.localtime())
        url = url_base.url_set_date_time + s
        return self.send_cmd(url)

    @staticmethod
    def download(last=True):
        try:
            logger.info("- download last one")
            url = settings.GOPRO_URL + settings.URL_MEDIA

            result = urllib2.urlopen(url, timeout=10).read()
            dirs = re.findall('href="(\d\d\dGOPRO)/"', result)
            if not dirs:
                logger.error("No Media Folders")
                return

            url += "/" + dirs[-1]
            result = urllib2.urlopen(url, timeout=10).read()
            pics = re.findall('href="(GOPR\d+\.JPG)"', result) + re.findall('href="(GOPR\d+\.MP4)"', result)
        except urllib2.URLError as e:
            logger.error(e)
            return

        if not pics:
            logger.error("No Pictures")
            return

        def download_pic(_url, _pic):
            _url += "/" + _pic
            _result = urllib2.urlopen(_url, timeout=10)
            f_name = '{}.000Z_{}'.format(datetime.datetime.now().replace(microsecond=0).isoformat(), _pic)
            logger.info("Downloading %s (%s bytes)..." % (f_name, _result.headers['content-length']))

            download_file_name = os.path.join(image_path, f_name)

            with open(download_file_name, "wb") as _f:
                while True:
                    chunk = _result.read(16 * 1024)
                    if not chunk:
                        break
                    _f.write(chunk)
                    print _f.tell(), "\r",
                    sys.stdout.flush()
            return download_file_name

        if last:
            return download_pic(url, max(pics))
        else:
            return [download_pic(url, pic) for pic in pics]

    def delete(self, last=True):
        logger.info("- delete")
        return self.send_cmd(url_base.url_delete_last if last else url_base.url_delete_all)


def push_picture_to_s3(_file_key, file_path):
    try:
        # connect to the bucket
        conn = boto.connect_s3(aws_key, aws_security)
        bucket = conn.get_bucket(aws_bucket)

        msg = "Uploading to AWS.. Key: " + _file_key + "  Path: " + file_path
        logger.info(msg)

        k = Key(bucket)
        k.key = _file_key
        k.set_contents_from_filename(file_path)
        # we need to make it public so it can be accessed publicly
        # using a URL like http://s3.amazonaws.com/bucket_name/key
        k.make_public()
        logger.info("Succeeded to upload to AWS S3...")
        return True

    except ValueError as e:
        logger.error(e)
    except socket.gaierror as e:
        logger.error(e)
    except boto.exception.S3ResponseError as e:
        logger.error(e)


if __name__ == '__main__':

    logger.debug('========== Starting GoPro {} Controller =========='.format(camera_type))

    delay = int(get_config('general', 'delay', 5))
    logger.debug('Sleeping for {} minutes'.format(delay))
    count_down(delay * 60)

    # Upload remaining image files
    for img in glob.glob(os.path.join(image_path, '*.JPG')):
        file_key = os.path.basename(img)
        pushed = push_picture_to_s3(_file_key=file_key, file_path=img)
        if pushed:
            logger.info('Pushed remaining image({}) to S3, removing...'.format(img))
            os.unlink(img)

    gopro = GoProCtrl()

#    gopro.wake()
    count_down(10)

    if get_config('general', 'take_photo', 'False').lower() == 'true':
        gopro.takepic()
        count_down(10)

    p_file_names = gopro.download(last=False)
    if p_file_names:
        logger.info('Downloaded {} file(s)'.format(len(p_file_names)))

        count_down(10)

        gopro.delete_all()

        count_down(10)

        for f in p_file_names:
            file_key = os.path.basename(f)
            pushed = push_picture_to_s3(_file_key=file_key, file_path=f)
            if pushed:
                os.unlink(f)

#    gopro.sleep()