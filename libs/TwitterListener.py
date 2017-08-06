from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API

from tweepy.streaming import StreamListener
from threading import Thread
import json
import logging


# These values are appropriately filled in the code
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


class StdOutListener( StreamListener ):

    def __init__( self, logger ):
        self.tweetCount = 0
        self.logger = logger

    def on_connect( self ):
        self.logger.info("Connection established!!")

    def on_disconnect( self, notice ):
        self.logger.error("Connection lost!! : {}".format(notice))

    def on_data( self, status ):
        self.logger.info("Entered on_data()")
        obj= json.loads(status)

        if 'direct_message' in obj:
            dm = obj['direct_message']
            sender = dm['sender']
            self.logger.info("<{}> {}: {}".format(dm['created_at'], sender['screen_name'], dm['text']))

        return True

    def on_direct_message( self, status ):
        self.on_data(status)

    def on_error( self, status ):
        print(status)


class TwitterListener (Thread):

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret, logger):
        super(TwitterListener, self).__init__()
        self.logger = logger

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.secure = True
            self.auth.set_access_token(access_key, access_secret)

            api = API(self.auth)

            # If the authentication was successful, you should
            # see the name of the account print out
            self.logger.info("Successfully authenticate with twitter account '{}'.".format(api.me().name))

        except BaseException as e:
            self.logger.error("Error in main()", e)

    def run(self):
        try:
            stream = Stream(self.auth, StdOutListener(self.logger) )

            stream.userstream()

        except BaseException as e:
            self.logger.error("Error in main()", e)