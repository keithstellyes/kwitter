import unittest
import setup_env

from logic.database.kw_database import KWDB
from logic.tools import generate_new_db
from logic.tweets.tweet import Tweet
from logic.users.tweeter_user import TweeterUser
from logic.shared import get_all
from logic.tools.kwdb_helper import connection

generate_new_db.generate_tables('testdir', 'sqlite3')
kwdb = KWDB(base_dir='testdir')
kwdb.connection = connection(kwdb)

class BasicCase(unittest.TestCase):
    def test_add_user_and_tweets(self):
        user = TweeterUser(handle='keith', user_id=1)
        kwdb.add(user)
        users = get_all.get_all_users(kwdb)
        self.assertEqual(len(users), 1)
        self.assertEqual(user.handle, 'keith')
        self.assertEqual(user.user_id, 1)
        t0 = Tweet(tweet_id=2, content='keith-tweet-id', user_id=1)
        t1 = Tweet(tweet_id=3, content='keith-tweet-handle', user_handle='keith')
        t2 = Tweet(tweet_id=4, content='#tag', user_id=1)
        tweets = [t0, t1, t2]
        for tweet in tweets:
            kwdb.add(tweet)
        tweets_results = get_all.get_all_tweets(kwdb)
        self.assertEqual(len(tweets_results), len(tweets))

        # get_all_tweets makes no guarantee on order
        if tweets_results[0].tweet_id == 2:
            t0_result = tweets_results[0]
            t1_result = tweets_results[1]
        else:
            t0_result = tweets_results[1]
            t1_result = tweets_results[0]

        self.assertGreaterEqual(t1_result.timestamp, t0_result.timestamp)
        self.assertEqual(t0_result.tweet_id, 2)
        self.assertEqual(t0_result.content, 'keith-tweet-id')
        self.assertEqual(t0_result.user_id, 1)

        self.assertEqual(t1_result.tweet_id, 3)
        self.assertEqual(t1_result.content, 'keith-tweet-handle')
        self.assertEqual(t1_result.user_id, 1)

        tags = get_all.get_all_tags(kwdb)
        self.assertEqual(len(tags), 1)
        tag = tags[0]
        self.assertEqual(tag.field, 'tag')
        self.assertEqual(tag.count, 1)

if __name__ == '__main__':
    unittest.main()