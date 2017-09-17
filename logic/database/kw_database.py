# sqlite3 is for debugging only
# its UUID's are only 64 bits instead of 128 bits like they ought to be
# typically will store connection object in .connection if relevant for db type

import json
import sqlite3
import os

from logic.shared import uuid as shared_uuid
from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException

KWDB_DEFAULT_FILENAME = 'kw.db'

class KWDB:
    # future: postgres
    # 0th index is default
    DB_TYPES = ['sqlite3']
    CONNECTOR_FUNCTIONS = {'sqlite3' : sqlite3.connect}

    def __init__(self, base_dir, db_filename=KWDB_DEFAULT_FILENAME, db_type=DB_TYPES[0]):
        self.db_type = db_type

        if not base_dir.endswith('/'):
            base_dir += '/'
        self.base_dir = base_dir
        self.__Connect = KWDB.CONNECTOR_FUNCTIONS[db_type]
        self.db_filename = db_filename


    def get_new_default_db(directory):
        return KWDB(directory)


    # returns json blob string
    # todo rename to "metadata_serialize
    def serialize(self):
        serialization = {}
        serialization['db_type'] = str(self.db_type)
        serialization['db_filepath'] = str(self.db_filepath())
        serialization['base_dir'] = str(self.base_dir)
        serialization['db_filename'] = str(self.db_filename)
        return json.dumps(serialization)

    # todo rename to metadata_deserialize
    def deserialize(directory):
        if not directory.endswith(os.sep):
            directory += os.sep
        blobstr = open(directory + 'metadata.json', 'r').read()
        blob = json.loads(blobstr)
        return KWDB(base_dir=blob['base_dir'], db_filename=blob['db_filename'], db_type=blob['db_type'])

    def db_filepath(self):
        return self.base_dir + self.db_filename

    # None to use default ID generation
    def get_id(self, clazz=None):
        if self.db_type == 'sqlite3':
            return int(shared_uuid.new_uuid()) % 2**32-1
        raise Exception

    def cursor(self):
        return self.connection.cursor()

    # If the object does not already have an ID, this will generate an ID.
    def add(self, item):
        item.__dbadd__(self)

    def adds(self, items):
        for item in items:
            self.add(item)

    def delete(self, item):
        item.__dbdel__(self)

    def commit(self):
        if self.db_type == 'sqlite3':
            self.connection.commit()
        else:
            raise UnsupportedDBTypeException(self.db_type)

def connect(kwdb):
    if kwdb.db_type == 'sqlite3':
        import sqlite3
        conn = sqlite3.connect(kwdb.db_filepath())
        kwdb.connection = conn
        return conn