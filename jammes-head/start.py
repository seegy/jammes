import configparser
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
# TODO import twitterhelper
# parent directory of script
parent_dir = os.path.dirname(sys.argv[0])

# load config
config = configparser.ConfigParser()


def reload_config():
    config.read([parent_dir + '/../config/sample-config.ini', parent_dir + '/../config/config.ini'])

reload_config()


# Logger
app_name = config.get('Jammes-Head', 'app-name', fallback='Jammes-Head')
log_level = config.get('Log', 'level', fallback='INFO')
log_file = config.get('Log', 'file', fallback='/tmp/jammes-head.log')
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=log_file,level=logging.getLevelName(log_level))
logger = logging.getLogger(app_name)
fh = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=5)
formatter = logging.Formatter(log_format)
fh.setFormatter(formatter)
fh.setLevel(logging.getLevelName(log_level))
logger.addHandler(fh)
