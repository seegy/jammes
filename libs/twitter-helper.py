import logging
import time
import uuid

import numpy as np
import tweepy
from past import autotranslate

autotranslate(['logging_twitter.handler'])
from logging_twitter.handler import TwitterHandler


class TwitterHelper:

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret, debug=False):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret
        self.debug = debug

        if not self.debug:
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_key, self.access_secret)
            self.tweet_api = tweepy.API(auth)

    def active_twitter_logger_for(self, target_twitter_user):

        # Add Twitter logging handler
        handler = TwitterHandler(consumer_key=self.consumer_key,
                                 consumer_secret=self.consumer_secret,
                                 access_token_key=self.access_key,
                                 access_token_secret=self.access_secret,
                                 direct_message_user=target_twitter_user)
        handler.setLevel(logging.ERROR)
        logging.addHandler(handler)

    def tweet(self, msg):
        msg = "{}\n({})\n{}".format(msg, time.strftime("%H:%M:%S", time.localtime()), str(uuid.uuid4())[:8])
        try:
            if not self.debug:
                self.tweet_api.update_status(msg)
            else:
                print(msg)
        except Exception as e:
            logging.error("Tweet went wrong: <{}> on tweet <{}> ".format(e, msg))

    def tweet_message(self, msg):
        msg = str(msg)

        # sum of character, a tweet can have
        TWEET_SIZE = 140
        # length of tweet-paging
        TWEET_APPEND_SIZE = len("...(x/x)")
        # the stuff from the 'tweet'-function to make every tweet unique
        TWEET_EXTENSION_SIZE = 20
        # length of message, that can really be used
        USABLE_TWEET_SIZE = TWEET_SIZE - TWEET_EXTENSION_SIZE
        # upper limit of message size
        MAX_TWEET_SIZE = 9 * (USABLE_TWEET_SIZE - TWEET_APPEND_SIZE)

        # cutting down to long messages
        if len(msg) > MAX_TWEET_SIZE:
            msg = msg[:MAX_TWEET_SIZE]

        # tweets to send
        tweets = []

        if len(msg) <= USABLE_TWEET_SIZE:
            tweets.append(msg)

        else:
            # iterator for messages
            i = 1
            # sum of messages
            msg_sum = int( np.ceil( len(msg) / float(USABLE_TWEET_SIZE - TWEET_APPEND_SIZE)))

            while len(msg) > 0:
                tweet_str = msg[ : USABLE_TWEET_SIZE - TWEET_APPEND_SIZE]

                if i != msg_sum:
                    tweet_str += "..."
                else:
                    tweet_str += " "

                tweet_str += "({}/{})".format(i, msg_sum)
                tweets.append( tweet_str )
                msg = msg[USABLE_TWEET_SIZE - TWEET_APPEND_SIZE :]
                i += 1

        for tweet in reversed(tweets):
            self.tweet(tweet)

