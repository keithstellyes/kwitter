from logic.users import tweeter_user


def add_user_auto(kwdb, user):
    if kwdb.db_type == 'sqlite3':
        add_user_auto_sqlite3(kwdb, user)
    else:
        raise UnsupportedDBException

def add_user_auto_sqlite3(kwdb, user):
    conn = kwdb.connection
    if user.user_id == None:
        user.user_id = kwdb.get_id(tweeter_user.TweeterUser)
    cursor = conn.cursor()
    if len(user.handle) > 50:
        raise Exception("Handles must be <= 50 characters")
    statement = 'INSERT INTO USERS(USER_ID, HANDLE) VALUES (?, ?)'

    cursor.execute(statement, (user.user_id, user.handle))
    conn.commit()

def get_username_from_id(kwdb, id):
    id = int(id)
    cursor = kwdb.cursor()
    return cursor.execute('select HANDLE from USERS where USER_ID=?', (id,)).fetchone()[0]

def get_id_from_username(kwdb, username):
    if type(username) != str:
        raise Exception
    cursor = kwdb.cursor()
    return cursor.execute('select USER_ID from USERS where HANDLE=?', (username,)).fetchone()[0]