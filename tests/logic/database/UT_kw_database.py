import unittest
import setup_env

from logic.database.kw_database import KWDB
from logic.tools import generate_new_db
from logic.tweets.tweet import Tweet
from logic.users.tweeter_user import TweeterUser
from logic.shared import get_all
from logic.tools.kwdb_helper import connection
from logic.followers.follower import Follower
from logic.shared import get_feed
from logic.users import user_management

generate_new_db.generate_tables('testdir', 'sqlite3')
kwdb = KWDB(base_dir='testdir')
kwdb.connection = connection(kwdb)

class BasicCase(unittest.TestCase):
    def test_add_user_and_tweets(self):
        user_keith = TweeterUser(handle='keith', user_id=1)
        kwdb.add(user_keith)
        users = get_all.get_all_users(kwdb)
        self.assertEqual(len(users), 1)
        self.assertEqual(user_keith.handle, 'keith')
        self.assertEqual(user_keith.user_id, 1)
        t0 = Tweet(tweet_id=2, content='keith-tweet-id', user_id=user_keith.user_id)
        t1 = Tweet(tweet_id=3, content='keith-tweet-handle', user_handle='keith')
        t2 = Tweet(tweet_id=4, content='#tag', user_id=user_keith.user_id)
        tweets = [t0, t1, t2]
        for tweet in tweets:
            kwdb.add(tweet)
        tweets_results = get_all.get_all_tweets(kwdb)
        self.assertEqual(len(tweets_results), len(tweets))

        t0_result = tweets_results[0]
        t1_result = tweets_results[1]

        self.assertGreaterEqual(t1_result.timestamp, t0_result.timestamp)
        self.assertEqual(t0_result.tweet_id, 2)
        self.assertEqual(t0_result.content, 'keith-tweet-id')
        self.assertEqual(t0_result.user_id, user_keith.user_id)

        self.assertEqual(t1_result.tweet_id, 3)
        self.assertEqual(t1_result.content, 'keith-tweet-handle')
        self.assertEqual(t1_result.user_id, user_keith.user_id)

        tags = get_all.get_all_tags(kwdb)
        self.assertEqual(len(tags), 1)
        tag = tags[0]
        self.assertEqual(tag.field, 'tag')
        self.assertEqual(tag.count, 1)

        user_kevin = TweeterUser(user_id=10, handle='kevin')
        kwdb.add(user_kevin)
        follower = Follower(followee_id=1, follower_id=10)
        kwdb.add(follower)
        feed = get_feed.get_feed_for_user_by_user_id(kwdb=kwdb, user_id=user_kevin.user_id)
        self.assertEqual(len(feed), 3)
        feed_index = 0
        expected_tweet_index = 2
        while expected_tweet_index >= 0:
            expect = tweets[expected_tweet_index]
            actual = feed[feed_index]
            self.assertEqual(actual.user_handle, 'keith')
            self.assertEqual(actual.content, expect.content)

            expected_tweet_index -= 1
            feed_index += 1
        feed = get_feed.get_feed_for_user_by_user_id(kwdb=kwdb, user_id=user_keith.user_id)
        self.assertEqual(len(feed), 0)

        #test ID generation
        user_logan = TweeterUser(handle='logan')
        kwdb.add(user_logan)
        logan_tweet = Tweet(content='logan-tweet', user_id=user_logan.user_id)
        kwdb.add(logan_tweet)

        tweets_results = get_all.get_all_tweets(kwdb)
        users_results = get_all.get_all_users(kwdb)
        logan_found = False
        user_logan_result = None

        for user in users_results:
            if user.handle is None:
                user.handle = user_management.get_username_from_id(kwdb, user.user_id)
            if user.handle == 'logan':
                logan_found = True
                user_logan_result = user
                break
        self.assertTrue(logan_found)

        logan_tweet_result = tweets_results[len(tweets_results) - 1]
        self.assertEqual(user_logan_result.user_id, user_logan.user_id)
        self.assertEqual(user_logan_result.handle, user_logan.handle)
        self.assertIsNotNone(user_logan.user_id)
        self.assertEqual(logan_tweet_result.content, logan_tweet.content)
        self.assertEqual(logan_tweet_result.tweet_id, logan_tweet.tweet_id)
        self.assertEqual(logan_tweet_result.user_id, user_logan.user_id)
        self.assertIsNotNone(logan_tweet.tweet_id)



if __name__ == '__main__':
    unittest.main()