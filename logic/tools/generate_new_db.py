import sqlite3
import setup_env
import os

from logic.database import kw_database
from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException
from logic.database.db_generation import generate_tables

import kw_globals

KWDB = kw_database.KWDB

DB_FILE_NAME = 'kw.db'

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