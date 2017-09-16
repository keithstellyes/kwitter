from logic.users import user_management
from logic.database.db_script_getter import read_db_script
from logic.tweets import tweet as tweet_module

class TweeterUser:
    def __init__(self, user_id=None, handle=None):
        self.user_id = user_id
        self.handle = handle

    def __conform__(self, protocol):
        pass

    def build_from_row(kwdb, row):
        if kwdb.db_type == 'sqlite3':
            return row
        else:
            raise Exception

    def build_from_row_sqlite3(row):
        id = TweeterUser._get_id_from_row_sqlite3(row)
        handle = TweeterUser._get_handle_from_row_sqlite3(row)
        return TweeterUser(id, handle)

    def build_from_rows_sqlite3(rows):
        return [TweeterUser.build_from_row_sqlite3(row) for row in rows]

    def _get_id_from_row_sqlite3(row):
        return row[0]

    def _get_handle_from_row_sqlite3(row):
        return row[1]

    def __str__(self):
        return str(self.handle) + ' (' + str(self.user_id) + ')'

    def __dbadd__(self, kwdb):
        user_management.add_user_auto(kwdb, self)

    def __dbdel__(self, kwdb):
        if self.user_id is None:
            self.user_id = user_management.get_id_from_username(kwdb, self.handle)
        tweet_id_script = read_db_script(['tweets', 'get-tweetids-of-userid.sql'])
        delete_user_script = read_db_script(['delete', 'delete-user.sql']).format(user_id=self.user_id)

        tweet_ids = kwdb.cursor().execute(tweet_id_script, (self.user_id,))
        tweet_ids = [int(tweet_id[0]) for tweet_id in tweet_ids]
        for tweet_id in tweet_ids:
            kwdb.delete(tweet_module.Tweet(tweet_id=tweet_id))
        kwdb.cursor().executescript(delete_user_script)
        kwdb.commit()
