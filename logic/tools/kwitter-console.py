from cmd import Cmd
import os
import sys
import shlex
import argparse

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
'''

add_tweet_parser = argparse.ArgumentParser(description='Add a tweet', prog='add tweet')
# if not specified, an automatic one will be generated.
add_tweet_parser.add_argument('-content')
add_tweet_parser.add_argument('-user_id')
add_tweet_parser.add_argument('-user_handle')
# tries -user_handle then -user_id
add_tweet_parser.add_argument('-user')
add_tweet_parser.add_argument('-tweet_id')
add_tweet_parser.add_argument('-user_handle')

add_follower_parser = argparse.ArgumentParser(description='Add a follower', prog='add follower')
add_follower_parser.add_argument('-follower_id')
add_follower_parser.add_argument('-follower_handle')
add_follower_parser.add_argument('-followee_id')
add_follower_parser.add_argument('-followee_handle')
# tries to match against a handle, then an ID. Convenient
add_follower_parser.add_argument('-follower')
add_follower_parser.add_argument('-followee')
add_follower_parser.add_argument('-mutual', help='Make them F4F')

add_user_parser = argparse.ArgumentParser(description='Add a user', prog='add user')

class KwitterConsole(Cmd):

    def __init__(self):
        super(KwitterConsole, self).__init__()
        self.prompt = '>>> '

    def emptyline(self):
        pass

    def do_add(self, arg):
        args = shlex.split(arg)
        if args[0] == 'tweet':
            add_tweet_parser.parse_args(args=args[1:])


if __name__ == '__main__':
    KwitterConsole().cmdloop('Kwitter Console')
