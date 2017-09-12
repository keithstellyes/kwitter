from logic.tags import tag_management
from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException

class TagTweet:
    def __init__(self, tag_id, tweet_id):
        self.tag_id = tag_id
        self.tweet_id = tweet_id

    def __dbadd__(self, kwdb):
        if kwdb.db_type == 'sqlite3':
            cursor = kwdb.cursor()
            cursor.execute('insert into TAG_TWEET(TAG_ID, TWEET_ID) values(?, ?)',
                           (self.tag_id, self.tweet_id))
            kwdb.connection.commit()
def construct_from_tweet(tweet):
    return [TagTweet(tag_id=tag.tag_id, tweet_id=tweet.tweet_id)
            for tag in tweet.tags]