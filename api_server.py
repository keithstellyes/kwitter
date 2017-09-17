import kw_globals
import os

kw_globals.SCRIPT_BASE_DIR = os.path.abspath(os.path.dirname(__file__))

from flask import Flask
from logic.shared import get_all
from logic.database.kw_database import KWDB, connect

import json

app = Flask(__name__)
kwdb = KWDB.deserialize(input('DB directory:'))
connect(kwdb)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/stream/<username>')
def feed(username):
    tweets = get_all.get_all_tweets_of_user_by_username(kwdb, username)
    return json.dumps([tweet.__jsonobj__() for tweet in tweets])

if __name__ == "__main__":
    app.run()