from cmd import Cmd
import os
import sys
import shlex
import argparse

import setup_env
from logic.tweets import tweet
from logic.users import tweeter_user
from logic.followers.follower import Follower
from logic.database.sanity_check import sanity_checker
from logic.database.db_script_getter import read_db_script
import kwdb_helper

def _exec(prog, arg):
    pipe = os.popen(sys.executable + ' ' + prog + ' ' + arg)
    print(pipe.read(), end='')
    pipe.close()

'''
main commands:

add - Adds an entity
del - Deletes an entity
get - Gets some entity type
db  - db tasks
db dump <table>
    dumps all "dependencies too"
db exec <command>
'''

add_tweet_parser = argparse.ArgumentParser(description='Add a tweet', prog='add tweet')
# if not specified, an automatic one will be generated.
add_tweet_parser.add_argument('-content')
add_tweet_parser.add_argument('-user_id')
add_tweet_parser.add_argument('-user_handle')
# tries -user_handle then -user_id
# add_tweet_parser.add_argument('-user')
add_tweet_parser.add_argument('-tweet_id')

add_follower_parser = argparse.ArgumentParser(description='Add a follower', prog='add follower')
add_follower_parser.add_argument('-follower_id')
add_follower_parser.add_argument('-follower_handle')
add_follower_parser.add_argument('-followee_id')
add_follower_parser.add_argument('-followee_handle')
# tries to match against a handle, then an ID. Convenient
# add_follower_parser.add_argument('-follower')
# add_follower_parser.add_argument('-followee')
add_follower_parser.add_argument('-mutual', help='Make them F4F')

add_user_parser = argparse.ArgumentParser(description='Add a user', prog='add user')
add_user_parser.add_argument('-user_id')
add_user_parser.add_argument('-handle')

get_tweet_parser = argparse.ArgumentParser(description='Get tweets', prog='get tweet')

db_sanity_parser = argparse.ArgumentParser(description='Check the sanity of a DB', prog='db sanity')
db_sanity_parser.add_argument('-include', action='append')
db_sanity_parser.add_argument('-exclude', action='append')
db_sanity_parser.add_argument('-list', action='store_true')

del_follower_parser = argparse.ArgumentParser(description='Removes a follower', prog='del follower')
del_follower_parser.add_argument('-follower_id')
del_follower_parser.add_argument('-followee_id')
del_follower_parser.add_argument('-follower_handle')
del_follower_parser.add_argument('-followee_handle')

del_user_parser = argparse.ArgumentParser(description='Deletes a user', prog='del user')
del_user_parser.add_argument('-handle')
del_user_parser.add_argument('-id')

get_follower_parser = argparse.ArgumentParser(description='Gets a user\'s followers', prog='get follower')
get_follower_parser.add_argument('-id')
get_follower_parser.add_argument('-handle')

get_followee_parser = get_follower_parser

class KwitterConsole(Cmd):
    def __init__(self, kwdb):
        super(KwitterConsole, self).__init__()
        self.prompt = '>>> '
        self.kwdb = kwdb

    def emptyline(self):
        pass

    def do_add(self, arg):
        try:
            args = shlex.split(arg)
            valid_opts = ['tweet', 'user', 'follower']
            if len(args) == 0 or args[0] not in valid_opts:
                print('`add\' needs an argument')
                print('one-of:\n' + '\n'.join(valid_opts))
            elif args[0] == 'tweet':
                parsed = vars(add_tweet_parser.parse_args(args=args[1:]))
                self.kwdb.add(tweet.Tweet(user_id=parsed['user_id'],
                                     user_handle=parsed['user_handle'],
                                     content=parsed['content'],
                                     tweet_id=parsed['tweet_id']))
            elif args[0] == 'user':
                parsed = vars(add_user_parser.parse_args(args=args[1:]))
                self.kwdb.add(tweeter_user.TweeterUser(user_id=parsed['user_id'],
                                                  handle=parsed['handle']))
            elif args[0] == 'follower':
                parsed = vars(add_follower_parser.parse_args(args=args[1:]))
                self.kwdb.add(Follower(follower_id=parsed['follower_id'],
                                       follower_handle=parsed['follower_handle'],
                                       followee_id=parsed['followee_id'],
                                       followee_handle=parsed['followee_handle']))
            else:
                print('Unrecognized option for `add\': ' + args[0])
        except:
            print(sys.exc_info())

    def do_del(self, arg):
        try:
            args = shlex.split(arg)
            valid_opts = ['follower', 'tweet', 'user']
            if len(args) == 0 or args[0] not in valid_opts:
                print('`del\' needs an argument')
                print('one-of:\n' + '\n'.join(valid_opts))
            elif args[0] == 'follower':
                parsed = vars(del_follower_parser.parse_args(args[1:]))
                follower = Follower(follower_id=parsed['follower_id'],
                                    followee_id=parsed['followee_id'],
                                    follower_handle=parsed['follower_handle'],
                                    followee_handle=parsed['followee_handle'])
                self.kwdb.delete(follower)
                self.kwdb.commit()
            elif args[0] == 'tweet':
                t = tweet.Tweet(tweet_id=int(args[1]))
                self.kwdb.delete(t)
                self.kwdb.commit()
            elif args[0] == 'user':
                parsed = vars(del_user_parser.parse_args(args=args[1:]))
                user = tweeter_user.TweeterUser(user_id=parsed['id'],
                                                handle=parsed['handle'])
                self.kwdb.delete(user)
        except:
            print(sys.exc_info())

    def do_get(self, arg):
        try:
            args = shlex.split(arg)
            valid_opts = ['tweet', 'user', 'follower', 'followee']

            if len(args) == 0 or args[0] not in valid_opts:
                print('`get\' needs an argument')
                print('one-of:\n' + '\n'.join(valid_opts))
            elif args[0] == 'tweet':
                from logic.shared.get_all import get_all_tweets
                from datetime import datetime
                from logic.users.user_management import get_username_from_id
                tweets = get_all_tweets(self.kwdb)
                for tweet in tweets:
                    tweet.user_handle = get_username_from_id(kwdb=self.kwdb, id=tweet.user_id)
                    print('"{content}" \n-{user_handle} @{timestamp}'.format(content=tweet.content,
                                                                             user_handle=tweet.user_handle,
                                                                             timestamp=datetime.fromtimestamp(
                                                                             tweet.timestamp)))
            elif args[0] == 'user':
                from logic.shared.get_all import get_all_users
                users = get_all_users(self.kwdb)
                for user in users:
                    print('{handle} ({id})'.format(handle=user.handle, id=user.user_id))
            elif args[0] == 'follower':
                parsed = vars(get_follower_parser.parse_args(args=args[1:]))
                user = tweeter_user.TweeterUser(handle=parsed['handle'],
                                                user_id=parsed['id'])

                from logic.shared.get_all import get_all_followers_of_user
                followers = get_all_followers_of_user(self.kwdb, user)
                print('Followers:\n{followers}'.format(
                    followers='\n'.join([follower.handle for follower in followers])))
            elif args[0] == 'followee':
                parsed = vars(get_followee_parser.parse_args(args=args[1:]))
                user = tweeter_user.TweeterUser(handle=parsed['handle'],
                                                user_id=parsed['id'])

                from logic.shared.get_all import get_all_followees_of_user
                followers = get_all_followees_of_user(self.kwdb, user)
                print('Followees:\n{followees}'.format(
                    followees='\n'.join([follower.handle for follower in followers])))
            else:
                print('Unrecognized option for `get\': ' + args[0])
        except:
            print(sys.exc_info())
    def do_db(self, arg):
        try:
            args = shlex.split(arg)
            valid_opts = ['generate', 'exec', 'type', 'sanity']
            if len(args) == 0 or args[0] not in valid_opts:
                print('`db\' needs an argument')
                print('one-of:\n' + '\n'.join(valid_opts))
            elif args[0] == 'generate':
                print('Ok, let\'s generate a DB for you')
                import logic.tools.generate_new_db
                logic.tools.generate_new_db.main()
            elif args[0] == 'exec':
                if args[1] == 'script':
                    script = open(args[2], 'r').read()
                    print('Executing query from:' + args[2])
                    rows = self.kwdb.cursor().executescript(script).fetchall()
                elif args[1] == 'file':
                    script = open(args[2], 'r').read()
                    print('Executing query from:' + args[2])
                    rows = self.kwdb.cursor().execute(script).fetchall()
                else:
                    query = ' '.join(args[1:])
                    print('Executing query: ' + query)
                    rows = self.kwdb.cursor().execute(query).fetchall()
                for row in rows:
                    row_str = [str(el) for el in row]
                    print('|'.join(row_str))
            elif args[0] == 'type':
                print('DB type: {db_type}'.format(db_type=self.kwdb.db_type))

            elif args[0] == 'sanity':
                rules = sanity_checker.ALL_RULES
                rule_map = {}
                [rule_map.__setitem__(rule.get_name(), rule) for rule in rules]
                parsed = vars(db_sanity_parser.parse_args(args=args[1:]))
                if parsed['list']:
                    print('Rules:')
                    [print(rule.get_name()) for rule in rules]
                    return
                rules_to_use = []
                if parsed['exclude'] is None and parsed['include'] is None:
                    rules_to_use = rules
                elif parsed['exclude'] is None and parsed['include'] is not None:
                    for rule in parsed['include']:
                        if rule not in rule_map.keys():
                            raise Exception('Unrecognized rule name:' + rule)
                        rules_to_use.append(rule_map[rule])
                elif parsed['exclude'] is not None and parsed['include'] is None:
                    for rule in parsed['exclude']:
                        if rule not in rule_map.keys():
                            raise Exception('Unrecognized rule name:' + rule)
                        del rule_map[rule]
                    rules_to_use = [rule_map[rule] for rule in rule_map.keys()]
                elif parsed['include'] is not None and parsed['exclude'] is not None:
                    raise Exception('Ambiguous arguments, given both includes and excludes')

                print('Using rules:')
                print('{rules}\n'.format(rules='\n'.join(
                    [rule.get_name() for rule in rules_to_use])))
                result = sanity_checker.sanitycheck(kwdb=self.kwdb, rules=rules_to_use)
                if result == []:
                    print('Ok')
                else:
                    for rule in result:
                        print('Rule failed: ' + rule.get_name())

            else:
                print('Unrecognized option for `db\': ' + args[0])
        except:
            print(sys.exc_info())

if __name__ == '__main__':
    KwitterConsole(kwdb_helper.prompt_for_db()).cmdloop('Kwitter Console')
