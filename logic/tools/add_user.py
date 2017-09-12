# DEPRECATED use the admin console instead.

import kwdb_helper

from logic.users.tweeter_user import TweeterUser

print('DEPRECATED use the admin console instead.')

db = kwdb_helper.prompt_for_db()
kwdb = db
conn = db.connection

while True:
    handle = input('Handle: ')
    kwdb.add(TweeterUser(handle=handle, user_id=None))