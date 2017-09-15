from logic.database.sanity_check.rule import SanityCheckRule
from logic.database.db_script_getter import read_db_script
from logic.database.unsupported_db_type_exception import UnsupportedDBTypeException

class RuleUniqueIDTemplate(SanityCheckRule):
    def get_name(self):
        pass
    def get_desc(self):
        pass
    def sanity_check(self, kwdb):
        pass

    def __init__(self, rule_name, entity_type, table_name, id_column):
        self.get_name_ret = rule_name
        self.get_desc_ret = \
            'Checks that all instances of {entity_type} have unique id\'s'\
                .format(entity_type=entity_type)
        self.sanity_check_script = read_db_script(
            ['sanity', 'uniqueid_template.sql'])\
            .format(table_name=table_name, id_column=id_column)

    def get_name(self):
        return self.get_name_ret

    def get_desc(self):
        return self.get_desc_ret

    def sanity_check(self, kwdb):
        if kwdb.db_type == 'sqlite3':
            return kwdb.cursor().execute(self.sanity_check_script).fetchall() == []
        else:
            raise UnsupportedDBTypeException(kwdb.db_type)

rule_uniqueid_tweet = RuleUniqueIDTemplate(rule_name='uniqueid_tweet',
                                           entity_type='tweet',
                                           table_name='TWEETS',
                                           id_column='TWEET_ID')

rule_uniqueid_user = RuleUniqueIDTemplate(rule_name='uniqueid_user',
                                           entity_type='user',
                                           table_name='USERS',
                                           id_column='USER_ID')

rule_uniqueid_tag = RuleUniqueIDTemplate(rule_name='uniqueid_tag',
                                         entity_type='tag',
                                         table_name='TAGS',
                                         id_column='TAG_ID')

rules = [rule_uniqueid_tag, rule_uniqueid_tweet, rule_uniqueid_user]