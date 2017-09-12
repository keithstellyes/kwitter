from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException
from logic.followers import follower_management

class Follower:
    def __init__(self, follower_id=None, followee_id=None, follower_handle=None, followee_handle=None):
        self.follower_id = follower_id
        self.followee_id = followee_id
        self.followee_handle = followee_handle
        self.follower_handle = follower_handle

    def build_from_row(row, kwdb):
        if kwdb.db_type == 'sqlite3':
            return Follower.build_from_row_sqlite3(row)
        else:
            raise UnsupportedDBTypeException
    def build_from_row_sqlite3(row):
        return Follower(Follower._get_follower_id_from_row_sqlite3(row),
                        Follower._get_followee_id_from_row_sqlite3(row))

    def _get_follower_id_from_row_sqlite3(row):
        return row[0]

    def _get_followee_id_from_row_sqlite3(row):
        return row[1]

    def __dbadd__(self, kwdb):
        follower_management.add_follower_auto(kwdb, self)