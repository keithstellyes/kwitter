from logic.tweets import tweet_management
from logic.shared import tagtweet
from logic.tags import tag_management
from logic.tags import tag as tag_module
from logic.users import user_management
from logic.database.db_script_getter import read_db_script
from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException

class Tweet:
    def __init__(self, user_id=None, content=None, timestamp=None, tweet_id=None, user_handle=None):
        self.user_id = user_id
        self.tweet_id = tweet_id
        self.content = content
        self.timestamp = timestamp
        if content is not None:
            tag_strs = tag_management.scan_tags_from_string(self.content)
            self.tags = [tag_module.Tag(field=tag_str) for tag_str in tag_strs]
        self.user_handle = user_handle

    def build_from_row(row):
        user_id = Tweet._get_user_id_from_row(row)
        tweet_id = Tweet._get_tweet_id_from_row(row)
        content = Tweet._get_content_from_row(row)
        timestamp = Tweet._get_timestamp_from_row(row)
        return Tweet(user_id, content, timestamp, tweet_id=tweet_id)

    def build_from_rows(rows):
        return [Tweet.build_from_row(row) for row in rows]

    def _get_user_id_from_row(row):
        return row[0]

    def _get_tweet_id_from_row(row):
        return row[1]

    def _get_content_from_row(row):
        return row[2]

    def _get_timestamp_from_row(row):
        return row[3]

    def __str__(self):

        s = '"{content}"\n@{timestamp} ({tweet_id}) - {user_id}'
        s = s.format(content=Tweet.__lpad__(self.content), timestamp=self.timestamp,
                     tweet_id=self.tweet_id, user_id=self.user_id)
        return s
    def __lpad__(s):
        try:
            return s + ' ' * (150 - len(s))
        except TypeError:
            return 'ERROR, NONE'

    def __dbadd__(self, kwdb):
        tweet_management.add_tweet_auto(kwdb, self)

    def __dbdel__(self, kwdb):
        if kwdb.db_type == 'sqlite3':
            tag_ids_script = read_db_script(['tweets', 'get-tagids-of-tweet.sql'])
            decrement_tag_script = read_db_script(['tweets', 'decrement-tag-byid.sql'])
            delete_tweet_script = read_db_script(['delete', 'delete-tweet.sql'])
            self.tweet_id = int(self.tweet_id)
            tag_ids = kwdb.cursor().execute(tag_ids_script, (self.tweet_id,)).fetchall()
            tag_ids = [tag_id[0] for tag_id in tag_ids]
            for tag_id in tag_ids:
                kwdb.cursor().execute(decrement_tag_script.replace('?', str(tag_id)))
            kwdb.cursor().executescript(delete_tweet_script.replace('?', str(self.tweet_id)))
        else:
            raise UnsupportedDBTypeException(kwdb.db_type)
