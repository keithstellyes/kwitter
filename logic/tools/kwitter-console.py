from cmd import Cmd
import os
import sys
import shlex
import argparse

import _fixpathing
from tweets import tweet
from users import tweeter_user
import kwdb_helper
import traceback

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
            valid_opts = ['tweet', 'user']
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
        except:
            print(sys.exc_info())
    def do_db(self, arg):
        args = shlex.split(arg)
        valid_opts = ['generate']
        if len(args) == 0 or args[0] not in valid_opts:
            print('`db\' needs an argument')
            print('one-of:\n' + '\n'.join(valid_opts))
        elif args[0] == 'generate':
            print('Ok, let\'s generate a DB for you')
            import generate_new_db

if __name__ == '__main__':
    KwitterConsole(kwdb_helper.prompt_for_db()).cmdloop('Kwitter Console')
