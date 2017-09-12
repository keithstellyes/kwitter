import sqlite3
import setup_env
import os

from logic.database import kw_database
from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException

import kw_globals

KWDB = kw_database.KWDB

DB_FILE_NAME = 'kw.db'

def generate_tables_sqlite3(conn):
    SCRIPT_BASE_DIR = kw_globals.SCRIPT_BASE_DIR
    path = os.path.join(SCRIPT_BASE_DIR, 'logic', 'database', 'dbinit-scripts', 'drop.sqlite3.sql')

    script = open(path, 'r').read()
    try:
        conn.cursor().executescript(script)
        conn.commit()
    except sqlite3.OperationalError:
        print('No tables were dropped.')

    path = os.path.join(SCRIPT_BASE_DIR, 'logic' ,'database', 'dbinit-scripts', 'init.sqlite3.sql')
    script = open(path, 'r').read()
    conn.cursor().executescript(script)
    conn.commit()
    conn.close()

def generate_tables(directory, db_type):
    db = KWDB(base_dir=directory, db_type=db_type)

    if db_type == 'sqlite3':
        generate_tables_sqlite3(sqlite3.connect(db.db_filepath()))
    print('Writing metadata')
    f = open(directory + 'metadata.json', 'w')
    f.write(db.serialize())
    f.close()

def main():
    db_option = input('Pick a DB option from: ' + str(KWDB.DB_TYPES) + ': ').strip().lower()

    if db_option not in KWDB.DB_TYPES:
        raise UnsupportedDBTypeException

    directory = input('Directory: ')

    if directory[len(directory ) - 1] != '/':
        directory += '/'

    generate_tables(directory, db_option)

    print('All done.')

if __name__ == '__main__':
    main()