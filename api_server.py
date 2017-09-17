import kw_globals
import os

kw_globals.SCRIPT_BASE_DIR = os.path.abspath(os.path.dirname(__file__))

from flask import Flask
from server.api import user_stream, tag_stream, user_feed
from logic.database.kw_database import KWDB, connect

import json

settings = json.load(open('api_server_settings.json', 'r'))

app = Flask(__name__)
kwdb = KWDB.deserialize(settings['db_path'])
connect(kwdb)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/stream/user/<username>')
def stream_username(username):
    return user_stream.user_stream_as_json(username=username, kwdb=kwdb)

@app.route('/stream/tag/<tag_field>')
def stream_tag(tag_field):
    return tag_stream.tag_stream_as_json(tag_field=tag_field,
                                         kwdb=kwdb)

@app.route('/feed/<username>')
def stream_user_feed(username):
    return user_feed.user_feed_as_json(username=username,
                                       kwdb=kwdb)

if __name__ == "__main__":
    app.run(host=settings['host'],
            port=settings['port'])