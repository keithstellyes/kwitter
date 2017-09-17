from logic.tags import tag_management, tag as tag_module
import json


def tag_stream_as_json(tag_field, kwdb):
    tweets = tag_management.get_all_tweets_with_tag(tag_module.Tag(field=tag_field),
                                           kwdb=kwdb)
    return json.dumps([tweet.__jsonobj__() for tweet in tweets])