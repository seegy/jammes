import configparser
import json
import os
import sys
from threading import Thread
from time import sleep

from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# parent directory of script
parent_dir = os.path.dirname(sys.argv[0])
config = configparser.ConfigParser()
config.read([parent_dir + '/../config/sample-config.ini', parent_dir + '/../config/config.ini'])

# These values are appropriately filled in the code
consumer_key = config.get('Twitter', 'consumer_key')
consumer_secret = config.get('Twitter', 'consumer_secret')
access_token = config.get('Twitter', 'access_token')
access_token_secret = config.get('Twitter', 'access_token_secret')


class StdOutListener( StreamListener ):

    def __init__( self ):
        self.isStopped = False

    def on_connect( self ):
        print("Connection established!!")

    def on_disconnect( self, notice ):
        print("Connection lost!! : ", notice)

    def on_data( self, status ):

        if self.isStopped:
            return False

        obj= json.loads(status)

        if 'direct_message' in obj:
            dm = obj['direct_message']
            sender = dm['sender']
            print("<{}> {}: {}".format(dm['created_at'], sender['screen_name'], dm['text']))

        return True

    def on_direct_message( self, status ):
       self.on_data()

    def on_error( self, status ):
        print("A problem occured: {}".format(status))

    def stop(self):
        self.isStopped = True


class TwitterListener (Thread):

    def __init__(self, auth):
        super(TwitterListener, self).__init__()
        self.listener = None
        self.auth = auth

    def run(self):
        try:
            self.listener = StdOutListener()
            stream = Stream(self.auth, self.listener)

            stream.userstream()

            print('Listening to Twitter finally stopped.')

        except BaseException as e:
            print("Error in main()", e)

    def stop(self):
        if self.listener is not None:
            print("disconnecting from Twitter")
            self.listener.stop()


class TwitterManager:

    def __init__(self):
        self.listener = None

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.secure = True
            self.auth.set_access_token(access_token, access_token_secret)

            api = API(self.auth)

            # If the authentication was successful, you should
            # see the name of the account print out
            print(api.me().name)

        except BaseException as e:
            print("Error in main()", e)

    def start_listener(self):
        self.listener = TwitterListener(self.auth)
        # twitter_listener.setName("TwitterListener")
        self.listener.start()

    def stop_listener(self):
        self.listener.stop()
        self.listener = None


def main():

    tm = TwitterManager()
    print("starting listener...")
    tm.start_listener()

    while True:
        sleep(10)
        print("stopping listener...")
        tm.stop_listener()
        sleep(5)
        print("starting listener...")
        tm.start_listener()


if __name__ == '__main__':
    main()
