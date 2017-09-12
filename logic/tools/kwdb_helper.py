import _fixpathing
from database import kw_database

global _conn
_conn = None
global _cursor
_cursor = None

def cursor(kwdb):
    global _cursor
    if _cursor != None:
        return _cursor
    if kwdb.db_type == 'sqlite3':
        _cursor = connection(kwdb).cursor()
        return _cursor

def connection(kwdb):
    global _conn
    if _conn != None:
        return _conn
    if kwdb.db_type == 'sqlite3':
        import sqlite3
        conn = sqlite3.connect(kwdb.db_filepath())
        _conn = conn
        return conn

def prompt_for_db():
    db_directory = input('Base DB directory (or blank to create one):').strip().rstrip('/') + '/'
    if db_directory == '/':
        print("Okay, let's generate a new database instead.")
        import generate_new_db
    kwdb = kw_database.KWDB.deserialize(db_directory)
    conn = connection(kwdb)
    kwdb.connection = conn

    return kwdb