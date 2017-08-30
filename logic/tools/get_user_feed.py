import _fixpathing

import kwdb_helper

from shared import get_feed
from users import user_management

from datetime import datetime

db = kwdb_helper.prompt_for_db()

while True:
    user_handle = input('Handle:')
    user_id = user_management.get_id_from_username(db, user_handle)
    feed_tweets = get_feed.get_feed_for_user_by_user_id(db, user_id)

    for tweet in feed_tweets:
        print('"{content}" \n-{user_handle} @{timestamp}'.format(content=tweet.content,
              user_handle=tweet.user_handle, timestamp=datetime.fromtimestamp(tweet.timestamp)))