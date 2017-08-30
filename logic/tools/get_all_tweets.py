import kwdb_helper

from shared import get_all

db = kwdb_helper.prompt_for_db()

tweets = get_all.get_all_tweets(db)

print('\n\n'.join([str(tweet) for tweet in tweets]))