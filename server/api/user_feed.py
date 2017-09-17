from logic.shared import get_feed
from logic.users.user_management import get_id_from_username

import json


# todo: This ought to be a query that doesn't require the user's ID
def user_feed_as_json(username, kwdb):
    id = get_id_from_username(kwdb=kwdb, username=username)
    feed = get_feed.get_feed_for_user_by_user_id(kwdb=kwdb,
                                                 user_id=id)
    return json.dumps([tweet.__jsonobj__() for tweet in feed])