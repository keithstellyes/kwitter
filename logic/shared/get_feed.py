from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException
from logic.tweets.tweet import Tweet
from logic.database.db_script_getter import read_db_script

#gets tweet's user, content and timestamp

def get_feed_for_user_by_user_id(kwdb, user_id):
    if kwdb.db_type == 'sqlite3':
        return get_feed_for_user_by_user_id_sqlite3(kwdb, user_id)
    else:
        raise UnsupportedDBTypeException(kwdb.db_type)


def get_feed_for_user_by_user_id_sqlite3(kwdb, user_id):
    query = read_db_script(['tweets', 'get-user-feed-via-userid.sql'])
    cursor = kwdb.cursor()
    cursor.execute(query, (int(user_id),))
    rows = cursor.fetchall()
    return [Tweet(user_handle=row[0],
                  content=row[1],
                  timestamp=row[2],
                  tweet_id=row[3]) for row in rows]

def get_feed_for_user_by_username_since(kwdb, username, since):
    if kwdb.db_type == 'sqlite3':
        return get_feed_for_user_by_username_since_sqlite3(kwdb, username, since)
    else:
        raise UnsupportedDBTypeException(kwdb.db_type)

def get_feed_for_user_by_username_since_sqlite3(kwdb, username, since):
    query = read_db_script(['tweets', 'get-user-feed-after-timestamp-via-username.sql'])
    cursor = kwdb.cursor()
    cursor.execute(query, (username, int(since)))
    rows = cursor.fetchall()
    return [Tweet(user_handle=row[0],
                 content=row[1],
                 timestamp=row[2],
                 user_id=row[3],
                 tweet_id=row[4]) for row in rows]