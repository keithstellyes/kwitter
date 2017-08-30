from tags import tag_management
from shared import tagtweet

class Tag:
    def __init__(self, field, tag_id=None, count=None):
        self.field = field
        self.tag_id = tag_id
        self.count = count

    def __dbadd__(self, kwdb):
        #if not tag_field_exists:
        tag_management.add_tag_auto(kwdb, self)

    def __str__(self):
        return str('#' + self.field + '(' + str(self.tag_id) + ')' + ' ' + str(self.count) + ' times')