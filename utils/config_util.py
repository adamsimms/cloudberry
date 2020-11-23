import ConfigParser
import os
import shutil

config = ConfigParser.RawConfigParser()

config_file = os.path.expanduser('~/cloudberry.ini')
if not os.path.exists(config_file):
    print 'No config file found! Copying default one'
    shutil.copy(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'config.ini'), config_file)


def get_config(section, option, default=None):
    try:
        config.read(config_file)
        return config.get(section=section, option=option)
    except ConfigParser.NoSectionError:
        return default
    except ConfigParser.NoOptionError:
        return default


def set_config(section, option, value):
    try:
        config.read(config_file)
    except Exception as e:
        print('Failed to read config file: {}'.format(e))
        return False

    if section not in config.sections():
        config.add_section(section=section)

    config.set(section=section, option=option, value=value)
    try:
        with open(config_file, 'w') as configfile:
            config.write(configfile)
        return True
    except Exception as e:
        print('Failed to write new config to file: {}'.format(e))
        return False


def get_section_config(section='picamera'):
    config.read(config_file)
    return {opt: config.get(section, opt) for opt in config.options(section)}
