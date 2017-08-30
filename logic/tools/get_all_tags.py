import kwdb_helper
from shared import get_all


db = kwdb_helper.prompt_for_db()

tags = get_all.get_all_tags(db)

print('\n\n'.join([str(tag) for tag in tags]))