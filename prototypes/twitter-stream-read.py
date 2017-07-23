from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API

from tweepy.streaming import StreamListener
import json

# These values are appropriately filled in the code
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

class StdOutListener( StreamListener ):

    def __init__( self ):
        self.tweetCount = 0

    def on_connect( self ):
        print("Connection established!!")

    def on_disconnect( self, notice ):
        print("Connection lost!! : ", notice)

    def on_data( self, status ):
        #print("Entered on_data()")

        obj= json.loads(status)

        if 'direct_message' in obj:
            dm = obj['direct_message']
            sender = dm['sender']
            print("<{}> {}: {}".format(dm['created_at'], sender['screen_name'], dm['text']), flush = True)

        return True

    def on_direct_message( self, status ):
        print("Entered on_direct_message()")
        try:
            print(status, flush = True)
            return True
        except BaseException as e:
            print("Failed on_direct_message()", str(e))

    def on_error( self, status ):
        print(status)


def main():

    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth.set_access_token(access_token, access_token_secret)

        api = API(auth)

        # If the authentication was successful, you should
        # see the name of the account print out
        print(api.me().name)

        stream = Stream(auth, StdOutListener())

        stream.userstream()
        print('?')

    except BaseException as e:
        print("Error in main()", e)

if __name__ == '__main__':
    main()