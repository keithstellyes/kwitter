'''
Rules, generally speaking, will be singletons.

Rule interface:

All rules must inhereit from SanityCheckRule

All rule modules should have a .rules, which is a list of its rules

e.g.

my_rule_module.rules
'''
class SanityCheckRule:
    # this should return a string that:
    # all chars are alphanumeric or are hyphens
    def get_name(self):
        raise NotImplementedError()

    # returns a human-readable string describing what this rule does.
    def get_desc(self):
        raise NotImplementedError()

    # Does a sanity check on the DB, returning true is it's OK, false otherwise
    def sanity_check(self, kwdb):
        raise NotImplementedError()