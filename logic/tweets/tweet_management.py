import time

from tags import tag as tag_module
from tags import tag_management
from tweets import tweet

from database.unsupported_db_type_exception import UnsupportedDBTypeException


def add_tweet_auto(kwdb, tweet_):
    if kwdb.db_type == 'sqlite3':
        add_tweet_sqlite3(kwdb, tweet_)
    else:
        raise UnsupportedDBTypeException

def add_tweet_sqlite3(kwdb, tweet_):
    conn = kwdb.connection
    if tweet_.tweet_id == None:
        tweet_.tweet_id = kwdb.get_id(tweet.Tweet)
    user_id = tweet_.user_id
    tweet_id = tweet_.tweet_id
    timestamp = int(time.time())
    content = tweet_.content

    cursor = conn.cursor()
    statement = 'insert into TWEETS(USER_ID, TWEET_ID, CONTENT, TIMESTAMP) values ' +\
                '(?, ?, ?, ?);'
    cursor.execute(statement, (user_id, tweet_id, content, timestamp))

    tags = tag_management.scan_tags_from_string(content)
    for tag_field in tags:
        if tag_management.get_tag_id(tag_field, kwdb) is None:
            kwdb.add(tag_module.Tag(field=tag_field))
    conn.commit()

def get_content_from_tweet_id(tweet_id, kwdb):
    cursor = kwdb.cursor()
    cursor.execute('select CONTENT from TWEETS where TWEET_ID=?', (tweet_id,))
    return cursor.fetchone()[0]