import kwdb_helper

from logic.shared import get_all
from logic.tags.tag_management import get_all_tweets_with_tag
from logic.tags.tag import Tag

db = kwdb_helper.prompt_for_db()

tag = Tag(field=input('Tag:'))

tweets = get_all_tweets_with_tag(tag=tag, kwdb=db)

for tweet in tweets:
    print(tweet.content)