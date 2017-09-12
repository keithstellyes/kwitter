# DEPRECATED use the admin console instead.

import time

import kwdb_helper
from logic.tweets import tweet_management
from logic.tweets.tweet import Tweet
from logic.users import user_management
from logic.tags import tag_management

print('DEPRECATED use the admin console instead.')

db = kwdb_helper.prompt_for_db()
kwdb = db
conn = db.connection

while True:
    handle = input('Handle: ')
    content = input('150 chars or less: ')
    while len(content) > 150:
        print('tweets must be <= 150 chars')
        content = input('150 chars or less: ')

    user_id = user_management.get_id_from_username(kwdb, handle)
    timestamp = int(time.time())

    kwdb.add(Tweet(user_id=user_id, content=content, timestamp=timestamp))
    tags = tag_management.scan_tags_from_string(content)

    print('Detected tags:' + str(tags))