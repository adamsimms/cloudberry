import sys
import time
import xmltodict
import datetime


def count_down(s):
    for i in range(s, 0, -1):
        print i,
        sys.stdout.flush()
        time.sleep(1)
    print


def get_serial():
    """
    Get serial number of the device
    :return:
    """
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26].lstrip('0')
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial


def parse_media_page(content):
    data = xmltodict.parse(content)
    tr_list = data['html']['body']['div']['div']['table']['tbody']['tr']
    if type(tr_list) != list:
        tr_list = [tr_list, ]
    images = []
    for tr in tr_list:
        v = {}
        for td in tr['td']:
            if 'a' in td:
                v['name'] = td['a']['#text']
            elif 'span' in td and type(td['span']) != list:
                v['date'] = datetime.datetime.strptime(td['span']['#text'], "%d-%b-%Y %H:%M")
        if '.JPG' in v['name'] or '.MP4' in v['name']:
            images.append(v)
    return sorted(images, key=lambda img: img['name'])


if __name__ == '__main__':
    _content = open('sample_response.xml').read()
    print(parse_media_page(_content))
