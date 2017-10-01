import kw_globals
import os

kw_globals.SCRIPT_BASE_DIR = os.path.abspath(os.path.dirname(__file__))

from flask import Flask, request
from server.api import user_stream, tag_stream, user_feed, follower_relations
from server.app_runner import run_app
from server import settings_loader
from logic.database.kw_database import KWDB, connect

settings = settings_loader.load_from_filepath('api_server_settings.json')

app = Flask(__name__)
kwdb = KWDB.deserialize(settings.db_path)
connect(kwdb)


@app.route('/')
def main_page():
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
    since = request.args.get('since')
    if since is None:
        return user_feed.user_feed_as_json(username=username,
                                       kwdb=kwdb)
    else:
        return user_feed.user_feed_as_json_since(kwdb=kwdb,
                                                 username=username,
                                                 since=since)

@app.route('/followers/<username>')
def get_followers_by_username(username):
    return follower_relations.get_followers_as_json(username=username,
                                                    kwdb=kwdb)


@app.route('/followees/<username>')
def get_followees_by_username(username):
    return follower_relations.get_followees_as_json(username=username,
                                                    kwdb=kwdb)

if __name__ == "__main__":
    run_app(app=app, settings=settings)
