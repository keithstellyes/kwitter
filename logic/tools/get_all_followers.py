import kwdb_helper
from logic.shared import get_all
from logic.users.user_management import get_username_from_id

db = kwdb_helper.prompt_for_db()

followers = get_all.get_all_followersrelations(db)

for follower in followers:
    followee_handle = get_username_from_id(db, follower.followee_id)
    follower_handle = get_username_from_id(db, follower.follower_id)

    print('{er} FOLLOWS {ee}'.format(ee=followee_handle, er=follower_handle))