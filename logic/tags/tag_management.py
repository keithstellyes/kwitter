from logic.tags import tag as tag_module

from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException
from logic.database.db_script_getter import read_db_script
from logic.tweets import tweet

def scan_tags_from_string(s):
    tags = []

    for i in range(len(s)):
        if s[i] != '#':
            continue

        i += 1
        tag = ''
        while i < len(s) and not s[i].isspace():
            tag += s[i]
            i += 1
        tags.append(tag)

    return tags

def get_tag_id(tag, kwdb):
    if kwdb.db_type == 'sqlite3':
        return get_tag_id_sqlite3(tag, kwdb)
    else:
        raise UnsupportedDBTypeException

def get_tag_id_sqlite3(tag, kwdb):
    cursor = kwdb.cursor()
    results = cursor.execute('select TAG_ID from TAGS where FIELD=?', (tag,))

    # returns None if no result

    row = results.fetchone()
    if row is None:
        return None
    return row[0]

def get_all_tweets_with_tag(tag, kwdb):
    if kwdb.db_type == 'sqlite3':
        return get_all_tweets_with_tag_sqlite3(tag, kwdb)
    else:
        raise UnsupportedDBTypeException

def get_all_tweets_with_tag_sqlite3(tag, kwdb):
    db_script = read_db_script(['tweets', 'get-tweets-via-tagfield.sql'])
    if tag.field is None:
        tag.field = get_tag_field_from_id(tag.tag_id)
    rows = kwdb.cursor().execute(db_script, (tag.field,))

    count = None
    tweets = []
    for row in rows:
        t = tweet.Tweet(content = row[0],
                        user_handle=row[1],
                        timestamp=row[2],
                        tweet_id=row[3],
                        user_id=row[4])
        t.count = row[5]
        tweets.append(t)


    return tweets

def get_tag_field_from_id(tag_id, kwdb):
    if kwdb.db_type == 'sqlite3':
        return get_tag_field_from_id_sqlite3(tag_id, kwdb)
    raise UnsupportedDBTypeException

def get_tag_field_from_id_sqlite3(tag_id, kwdb):
    cursor = kwdb.cursor()
    statement = 'select FIELD from TAGS where TAG_ID=?'
    row = cursor.execute(statement, (int(tag_id),))
    if row is not None:
        return row[0]
    else:
        return None

def add_tag_auto(kwdb, tag):
    if kwdb.db_type == 'sqlite3':
        add_tag_auto_sqlite3(kwdb, tag)
    else:
        raise UnsupportedDBTypeException

def add_tag_auto_sqlite3(kwdb, tag):
    cursor = kwdb.cursor()
    if tag.tag_id is None:
        tag.tag_id = get_tag_id(tag=tag.field, kwdb=kwdb)
        if tag.tag_id is None:
            tag.tag_id = kwdb.get_id(tag_module.Tag)
    tagcount = get_tag_count_sqlite3(kwdb, tag)
    tagcount += 1
    # in other words, was the tag already here?
    if tagcount > 1:
        cursor.execute('delete from TAGS where TAG_ID=?', (tag.tag_id,))
    cursor.execute('insert into TAGS(TAG_ID, FIELD, COUNT) values(?, ?, ?)',
                   (tag.tag_id, tag.field, tagcount))
    kwdb.connection.commit()


def get_tag_count_sqlite3(kwdb, tag):
    cursor = kwdb.cursor()
    cursor.execute('select COUNT from TAGS where TAG_ID=?', (tag.tag_id,))
    row = cursor.fetchone()
    if row is None:
        return 0
    return row[0]