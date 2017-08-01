import configparser
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from libs import TwitterHelper as th
from time import sleep
from libs import TwitterListener as tl

DEBUG = False

# parent directory of script
parent_dir = os.path.dirname(sys.argv[0])

# load config
config = configparser.ConfigParser()


def reload_config():
    config.read([parent_dir + '/../config/sample-config.ini', parent_dir + '/../config/config.ini'])


reload_config()

# init twitter helper for tweets and error loggings
twitter = th.TwitterHelper(config.get('Twitter', 'consumer_key'),
                           config.get('Twitter', 'consumer_secret'),
                           config.get('Twitter', 'access_token'),
                           config.get('Twitter', 'access_token_secret'),
                           debug=DEBUG)

# read and create logger configs
app_name = config.get('Jammes-Head', 'app-name', fallback='Jammes-Head')
log_level = config.get('Log', 'level', fallback='INFO')
log_file = config.get('Log', 'file', fallback='/tmp/jammes-head.log')
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# create logger
logging.basicConfig(filename=log_file, level=logging.getLevelName(log_level))
logger = logging.getLogger(app_name)

# create file handler
fh = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=5)
fh.setLevel(logging.getLevelName(log_level))

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter for both handlers
formatter = logging.Formatter(log_format)
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# adding handler
logger.addHandler(fh)
logger.addHandler(ch)

if config.getboolean('Twitter', 'log_via_twitter', fallback=False):
    twitter.active_twitter_logger_for(app_name, config.get('Twitter', 'log_target_user', fallback=''))


def main():

    # init twitter listener
    twitter_listener = tl.TwitterListener(config.get('Twitter', 'consumer_key'),
                                          config.get('Twitter', 'consumer_secret'),
                                          config.get('Twitter', 'access_token'),
                                          config.get('Twitter', 'access_token_secret'),
                                          logger)
    twitter_listener.setName("TwitterListener")
    twitter_listener.start()

    logger.info("TwitterListener initialized.")

    # TODO ?

    while True:
        sleep(1)
    pass

if __name__ == "__main__":
    main()
