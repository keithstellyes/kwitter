import kwdb_helper

from shared import get_all

db = kwdb_helper.prompt_for_db()

users = get_all.get_all_users(db)

users = [str(user) for user in users]

print('\n\n'.join(users))