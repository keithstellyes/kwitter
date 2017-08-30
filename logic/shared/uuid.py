import uuid

def new_uuid():
    result = uuid.uuid4()
    while result == 0:
        result = uuid.uuid4()
    return result