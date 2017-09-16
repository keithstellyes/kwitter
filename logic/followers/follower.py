from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException
from logic.followers import follower_management
from logic.database.db_script_getter import read_db_script
from logic.users.user_management import get_id_from_username, get_username_from_id

class FollowerRelation:
    def __init__(self, follower_id=None, followee_id=None, follower_handle=None, followee_handle=None):
        self.follower_id = follower_id
        self.followee_id = followee_id
        self.followee_handle = followee_handle
        self.follower_handle = follower_handle

    def build_from_row(row, kwdb):
        if kwdb.db_type == 'sqlite3':
            return FollowerRelation.build_from_row_sqlite3(row)
        else:
            raise UnsupportedDBTypeException

    def fill_fields(self, kwdb):
        if self.follower_id is None:
            self.follower_id = get_id_from_username(kwdb, self.follower_handle)
        if self.followee_id is None:
            self.followee_id = get_id_from_username(kwdb, self.followee_handle)
        if self.follower_handle is None:
            self.follower_handle = get_username_from_id(kwdb, self.follower_id)
        if self.followee_handle is None:
            self.followee_handle = get_username_from_id(kwdb, self.followee_id)

    def build_from_row_sqlite3(row):
        return FollowerRelation(FollowerRelation._get_follower_id_from_row_sqlite3(row),
                                FollowerRelation._get_followee_id_from_row_sqlite3(row))

    def _get_follower_id_from_row_sqlite3(row):
        return row[0]

    def _get_followee_id_from_row_sqlite3(row):
        return row[1]

    def __dbadd__(self, kwdb):
        follower_management.add_followerrelation_auto(kwdb, self)

    def __dbdel__(self, kwdb):
        script = read_db_script(['delete', 'delete-follower.sql'])
        self.fill_fields(kwdb)
        kwdb.cursor().execute(script, (self.follower_id, self.followee_id))