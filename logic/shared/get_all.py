'''
This is intended for debug or for tools.

Normally, this probably shouldn't be called...
'''

from logic.tweets import tweet
from logic.users import tweeter_user, user_management
from logic.tags import tag as tag_module
from logic.followers.follower import Follower
from logic.shared.tagtweet import TagTweet
from logic.database.db_script_getter import read_db_script
from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException


def get_all_users(kwdb):
    if kwdb.db_type == 'sqlite3':
        return get_all_users_sqlite3(kwdb)
    else:
        raise UnsupportedDBTypeException

def get_all_users_sqlite3(kwdb):
    cursor = kwdb.cursor()
    rows = cursor.execute('select * from USERS').fetchall()
    return [tweeter_user.TweeterUser.build_from_row_sqlite3(row) for row in rows]

def get_all_tweets(kwdb):
    if kwdb.db_type == 'sqlite3':
        return get_all_tweets_sqlite3(kwdb)
    else:
        raise UnsupportedDBTypeException(kwdb.db_type)

def get_all_tags(kwdb):
    if kwdb.db_type == 'sqlite3':
        return get_all_tags_sqlite3(kwdb)
    else:
        raise UnsupportedDBTypeException(kwdb.db_type)

def get_all_tags_sqlite3(kwdb):
    cursor = kwdb.cursor()
    rows = cursor.execute('select TAG_ID, FIELD, COUNT from TAGS').fetchall()
    return [tag_module.Tag(tag_id=row[0], field=row[1], count=row[2]) for row in rows]

def get_all_tweets_sqlite3(kwdb):
    cursor = kwdb.cursor()
    rows = cursor.execute('select USER_ID, TWEET_ID, CONTENT, TIMESTAMP from TWEETS').fetchall()
    return [tweet.Tweet.build_from_row(row) for row in rows]

def get_all_followers(kwdb):
    if kwdb.db_type == 'sqlite3':
        return get_all_followers_sqlite3(kwdb)
    else:
        raise UnsupportedDBTypeException(kwdb.db_type)

def get_all_followers_sqlite3(kwdb):
    cursor = kwdb.cursor()
    rows = cursor.execute('select FOLLOWEE_ID, FOLLOWER_ID from FOLLOWERS').fetchall()
    return [Follower(followee_id=row[0], follower_id=row[1]) for row in rows]

def get_all_followers_of_user(kwdb, user):
    if kwdb.db_type == 'sqlite3':
        return get_all_followers_of_user_sqlite3(kwdb, user)
    else:
        raise UnsupportedDBTypeException(kwdb.db_type)

def get_all_followers_of_user_sqlite3(kwdb, user):
    script = read_db_script(['followers', 'get-followers-by-followeeid.sql'])
    if user.user_id is None:
        user.user_id = user_management.get_id_from_username(kwdb, user.handle)
    rows = kwdb.cursor().execute(script, (user.user_id,))
    return [tweeter_user.TweeterUser(handle=row[0],
                                     user_id=row[1]) for row in rows]


def get_all_followees_of_user(kwdb, user):
    if kwdb.db_type == 'sqlite3':
        return get_all_followees_of_user_sqlite3(kwdb, user)
    else:
        raise UnsupportedDBTypeException(kwdb.db_type)

def get_all_followees_of_user_sqlite3(kwdb, user):
    script = read_db_script(['followers', 'get-followees-by-followerid.sql'])
    if user.user_id is None:
        user.user_id = user_management.get_id_from_username(kwdb, user.handle)
    rows = kwdb.cursor().execute(script, (user.user_id,))
    return [tweeter_user.TweeterUser(handle=row[0],
                                     user_id=row[1]) for row in rows]