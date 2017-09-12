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
    def test_add_user(self):
        user = TweeterUser(handle='keith', user_id=1)
        kwdb.add(user)
        users = get_all.get_all_users(kwdb)
        self.assertEqual(len(users), 1)
        self.assertEqual(user.handle, 'keith')
        self.assertEqual(user.user_id, 1)

if __name__ == '__main__':
    unittest.main()