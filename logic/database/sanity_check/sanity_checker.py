# Sanity checking rules:
# All entity types must have unique ID's.
#   e.g. all entires in tweets table have unique ID
# All tag COUNTs must be correct
from logic.database.sanity_check import rule_uniqueid

ALL_RULES = [] + rule_uniqueid.rules

# returns failed rules
def sanitycheck(kwdb, rules=ALL_RULES):
    failed_rules = []
    for rule in rules:
        if not rule.sanity_check(kwdb):
            failed_rules.append(rule)
    return failed_rules