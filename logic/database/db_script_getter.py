import sys
import os
import kw_globals

DB_SCRIPT_PATH = os.path.join(kw_globals.SCRIPT_BASE_DIR, 'logic', 'database', 'scripts')

def read_db_script(filename_or_filepaths):
    if type(filename_or_filepaths) == list:
        filename = os.path.join(*filename_or_filepaths)
        filename = os.path.join(DB_SCRIPT_PATH, filename)
    else:
        filename = filename_or_filepaths
    f = open(filename, 'r')
    script = f.read()
    f.close()
    return script
