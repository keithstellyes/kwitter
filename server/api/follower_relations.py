from logic.shared.get_all import get_all_followees_of_user_by_username,\
                                 get_all_followers_of_user_by_username

import json


def get_followers_as_json(username, kwdb):
    users = get_all_followers_of_user_by_username(kwdb=kwdb,
                                                  username=username)
    return json.dumps([user.__jsonobj__() for user in users])

def get_followees_as_json(username, kwdb):
    users = get_all_followees_of_user_by_username(kwdb=kwdb,
                                                  username=username)
    return json.dumps([user.__jsonobj__() for user in users])