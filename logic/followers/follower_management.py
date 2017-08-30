from users.user_management import get_id_from_username
from users.user_management import get_username_from_id

from database.unsupported_db_type_exception import UnsupportedDBTypeException


def add_follower_auto(kwdb, follower):
    follower_id = follower.follower_id
    followee_id = follower.followee_id
    follower_id = int(follower_id)
    followee_id = int(followee_id)
    if kwdb.db_type == 'sqlite3':
        add_follower_auto_sqlite3(kwdb, follower_id, followee_id)
    else:
        raise UnsupportedDBTypeException

def add_follower_auto_sqlite3(kwdb, follower_id, followee_id):
    cursor = kwdb.cursor()
    cursor.execute('insert into FOLLOWERS(FOLLOWER_ID, FOLLOWEE_ID) values (?, ?)', (int(follower_id), int(followee_id)))
    kwdb.connection.commit()

#todo do it better
def get_followerids_by_handle(kwdb, followee_handle):
    followee_id = get_id_from_username(kwdb, followee_handle)
    return get_followerids_by_id(kwdb, followee_id)

def get_followerids_by_id(kwdb, followee_id):
    cursor = kwdb.cursor()
    cursor.execute('select FOLLOWER_ID from FOLLOWERS where FOLLOWEE_ID=?', (followee_id,))
    rows = cursor.fetchall()
    followers = [row[0] for row in rows]
    return followers

#todo do it better
'''
select HANDLE from ( 
    select FOLLOWER_ID from FOLLOWERS where FOLLOWEE_ID=?
) inner join USERS on USERS.USER_ID=FOLLOWER_ID;
'''
def get_followerhandles_by_handle(kwdb, followee_handle):
    follower_ids = get_followerids_by_handle(kwdb, followee_handle)
    return [get_username_from_id(kwdb, id) for id in follower_ids]