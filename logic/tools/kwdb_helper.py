import setup_env
from logic.database import kw_database

def prompt_for_db():
    db_directory = input('Base DB directory (or blank to create one):').strip().rstrip('/') + '/'
    if db_directory == '/':
        print("Okay, let's generate a new database instead.")
        import generate_new_db
        generate_new_db.main()
    kwdb = kw_database.KWDB.deserialize(db_directory)
    conn = kw_database.connect(kwdb)
    kwdb.connection = conn

    return kwdb