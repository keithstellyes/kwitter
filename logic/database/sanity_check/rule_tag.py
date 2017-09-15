from logic.database.sanity_check.rule import SanityCheckRule
from logic.shared.get_all import get_all_tags, get_all_tweets
from logic.tags.tag_management import scan_tags_from_string, get_all_tweets_with_tag
from logic.database.db_script_getter import read_db_script


class TagCountRule(SanityCheckRule):
    def get_name(self):
        return 'tag_count'
    def get_desc(self):
        return 'Checks that all tags have the current count'

    def __check_tag(tag, tweets):
        count_stored = tag.count
        count_actual = 0
        for tweet in tweets:
            if tag.field in tweet.tags:
                count_actual += 1
        return count_stored == count_actual

    def sanity_check(self, kwdb):
        tweets = get_all_tweets(kwdb)
        tags = get_all_tags(kwdb)
        for tweet in tweets:
            tweet.tags = scan_tags_from_string(tweet.content)
        for tag in tags:
            if not TagCountRule.__check_tag(tag, tweets):
                return False
        return True


class TagTweetIntersectionRule(SanityCheckRule):
    def get_name(self):
        return 'tag_tweet_intersection_count'
    def get_desc(self):
        return 'Checks that all tweets and tags have their proper entries in the intersection table'
    def sanity_check(self, kwdb):
        tweets = get_all_tweets(kwdb)
        tags = get_all_tags(kwdb)
        for tag in tags:
            my_tweets_generated = []
            for tweet in tweets:
                if tag.field in scan_tags_from_string(tweet.content):
                    my_tweets_generated.append(tweet)
            my_tweets_stored = get_all_tweets_with_tag(tag, kwdb)
            my_tweets_generated = sorted([gentweet.tweet_id for gentweet in my_tweets_generated])
            my_tweets_stored = sorted([storetweet.tweet_id for storetweet in my_tweets_stored])
            if not my_tweets_stored == my_tweets_generated:
                return False
        return True

class TagTweetIntersectionUnique(SanityCheckRule):
    def get_name(self):
        return 'tag_tweet_intersection_duplicate'
    def get_desc(self):
        return 'Checks there are no duplicate entries in the intersection table'
    def sanity_check(self, kwdb):
        script = read_db_script(['sanity', 'unique_tagtweet.sql'])
        return kwdb.cursor().execute(script).fetchall() == []

rules = [TagCountRule(), TagTweetIntersectionRule(), TagTweetIntersectionUnique()]