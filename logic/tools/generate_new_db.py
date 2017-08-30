import sqlite3
import _fixpathing

from database import kw_database

from database.unsupported_db_type_exception import UnsupportedDBTypeException

KWDB = kw_database.KWDB

DB_FILE_NAME = 'kw.db'

def generate_tables_sqlite3(conn):
    script = open('../database/dbinit-scripts/drop.sqlite3.sql', 'r').read()
    try:
        conn.cursor().executescript(script)
        conn.commit()
    except sqlite3.OperationalError:
        print('No tables were dropped.')

    script = open('../database/dbinit-scripts/init.sqlite3.sql', 'r').read()
    conn.cursor().executescript(script)
    conn.commit()
    conn.close()

def generate_tables(directory, db_type):
    db = KWDB(base_dir=directory, db_filename=DB_FILE_NAME, db_type=db_type)

    if db_type == 'sqlite3':
        generate_tables_sqlite3(sqlite3.connect(db.db_filepath()))
    print('Writing metadata')
    f = open(directory + 'metadata.json', 'w')
    f.write(db.serialize())
    f.close()


db_option = input('Pick a DB option from: ' + str(KWDB.DB_TYPES) + ': ').strip().lower()

if db_option not in KWDB.DB_TYPES:
    raise UnsupportedDBTypeException

directory = input('Directory: ')

if directory[len(directory ) - 1] != '/':
    directory += '/'

generate_tables(directory, db_option)

print('All done.')