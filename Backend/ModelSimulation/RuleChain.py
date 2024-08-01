# Used for propensity caching - given a rule, find all rules that require an updated propensity

def ruleToClasses(rules, locations, matched_indices):

def classToRule(rules, locations, matched_indices):

# Returns a dictionary that maps a rule index to a set of all rule indices that have a changed propensity after a rule trigger.
def ruleToRule(rtc_dict, ctr_dict):
    rtr_dict = {rule_location_key : set([])for rule_location_key in list(rtc_dict.keys())}

    for rule_location_key in list(rtr_dict.keys()):
        for class_loc in rtc_dict[rule_location_key]:
            rtr_dict[rule_location_key].add(ctr_dict[class_loc])
    return rtr_dict

def returnOneStepRuleUpdate(rules, locations, matched_indices):
    rtc_dict = ruleToClasses()
    ctr_dict = classToRule()
    return ruleToRule(rtc_dict, ctr_dict)
