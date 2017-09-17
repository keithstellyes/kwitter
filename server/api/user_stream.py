from logic.shared import get_all
import json

def user_stream_as_json(username, kwdb):
    tweets = get_all.get_all_tweets_of_user_by_username(kwdb, username)
    return json.dumps([tweet.__jsonobj__() for tweet in tweets])