import json

class Settings:
    pass

def load_from_filepath(filepath):
    settings = Settings()
    settings.__dict__ = json.load(open(filepath, 'r'))
    return settings

def load_from_jsonstr(jsonstr):
    settings = Settings()
    settings.__dict__ = json.loads(jsonstr)

    return settings