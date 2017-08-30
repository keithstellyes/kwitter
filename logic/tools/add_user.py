import kwdb_helper

from users.tweeter_user import TweeterUser

db = kwdb_helper.prompt_for_db()
kwdb = db
conn = db.connection

while True:
    handle = input('Handle: ')
    kwdb.add(TweeterUser(handle=handle, user_id=None))