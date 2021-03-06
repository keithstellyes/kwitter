import time

from logic.tags import tag as tag_module
from logic.tags import tag_management
from logic.tweets import tweet
from logic.users import user_management
from logic.shared import tagtweet

from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException


def add_tweet_auto(kwdb, tweet_):
    if kwdb.db_type == 'sqlite3':
        add_tweet_sqlite3(kwdb, tweet_)
    else:
        raise UnsupportedDBTypeException

def add_tweet_sqlite3(kwdb, tweet_):
    conn = kwdb.connection
    if tweet_.tweet_id is None:
        tweet_.tweet_id = kwdb.get_id(tweet.Tweet)
    user_id = tweet_.user_id

    if user_id is None and tweet_.user_handle is not None:
        user_id = user_management.get_id_from_username(kwdb, tweet_.user_handle)

    tweet_id = tweet_.tweet_id
    if tweet_.timestamp is None:
        tweet_.timestamp = int(time.time())
    timestamp = tweet_.timestamp
    content = tweet_.content

    cursor = conn.cursor()
    statement = 'insert into TWEETS(USER_ID, TWEET_ID, CONTENT, TIMESTAMP) values ' +\
                '(?, ?, ?, ?);'
    cursor.execute(statement, (user_id, tweet_id, content, timestamp))

    tags = tag_management.scan_tags_from_string(content)
    for tag_field in tags:
        tag = tag_module.Tag(field=tag_field)
        kwdb.add(tag)
        kwdb.add(tagtweet.TagTweet(tag_id=tag.tag_id, tweet_id=tweet_.tweet_id))
    conn.commit()

def get_content_from_tweet_id(tweet_id, kwdb):
    cursor = kwdb.cursor()
    cursor.execute('select CONTENT from TWEETS where TWEET_ID=?', (tweet_id,))
    return cursor.fetchone()[0]