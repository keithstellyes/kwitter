import _fixpathing

from followers import follower_management

from tools import kwdb_helper

db = kwdb_helper.prompt_for_db()
kwdb = db
conn = db.connection

while True:
    name = input('Get my followers:')
    print('\n'.join(follower_management.get_followerhandles_by_handle(kwdb, name)))