import sys
import time


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
