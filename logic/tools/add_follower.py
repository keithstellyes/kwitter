import setup_env

from logic.followers.follower import FollowerRelation
from logic.users import user_management

import kwdb_helper

db = kwdb_helper.prompt_for_db()
kwdb = db
conn = db.connection

while True:
    follower_handle = input('Follower:')
    followee_handle = input('Followee:')
    follower_id = user_management.get_id_from_username(kwdb, follower_handle)
    followee_id = user_management.get_id_from_username(kwdb, followee_handle)

    kwdb.add(FollowerRelation(follower_id, followee_id))