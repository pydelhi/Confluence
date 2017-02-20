# Twitter tokens
from confluence.settings import TWITTER_CONSUMER_KEY
from confluence.settings import TWITTER_CONSUMER_SECRET
from confluence.settings import TWITTER_ACCESS_KEY
from confluence.settings import TWITTER_ACCESS_SECRET

# Tweepy helps in accessing Twitter via Basic Authentication and OAuth
import tweepy


def twitter_api_authentication():
    """
    Return authentication for twitter using tweepy, authenticated via
    TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_KEY and
    TWITTER_ACCESS_SECRET.
    """
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
    return tweepy.API(auth)
