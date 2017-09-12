from logic.database.kw_database import KWDB
from logic.database.db_script_getter import read_db_script
import sqlite3

def generate_tables_sqlite3(conn):
    script = read_db_script(['init', 'drop.sqlite3.sql'])
    try:
        conn.cursor().executescript(script)
        conn.commit()
    except sqlite3.OperationalError:
        print('No tables were dropped.')

    script = read_db_script(['init', 'init.sqlite3.sql'])
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