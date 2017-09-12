from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException
from logic.tweets.tweet import Tweet


#gets tweet's user, content and timestamp

def get_feed_for_user_by_user_id(kwdb, user_id):
    if kwdb.db_type == 'sqlite3':
        return get_feed_for_user_by_user_id_sqlite3(kwdb, user_id)
    else:
        raise UnsupportedDBTypeException


def get_feed_for_user_by_user_id_sqlite3(kwdb, user_id):
    query = '''-- get the tweet content and timestamp, dropping the ID information
select HANDLE,CONTENT,TIMESTAMP from (
-- get the handles for all those ID's
    select HANDLE, FOLLOWEE_ID from (
-- get the ID's of all followers
        select FOLLOWEE_ID from FOLLOWERS where FOLLOWER_ID=?
    ) inner join USERS on USERS.USER_ID=FOLLOWEE_ID
) inner join TWEETS on FOLLOWEE_ID=TWEETS.USER_ID order by TIMESTAMP desc;'''
    cursor = kwdb.cursor()
    cursor.execute(query, (int(user_id),))
    rows = cursor.fetchall()
    return [Tweet(user_handle=row[0], content=row[1], timestamp=row[2]) for row in rows]