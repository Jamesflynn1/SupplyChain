def isSubtypeOf(parent_type, child_type):
    # Equality for the moment
    return parent_type == child_type

def writeMatchedRuleJSON(rules, locations):
    # For each rule, on each type that matches a general type

    filled_rules = {i:[] for i in range(len(rules))}
    for rule_i in range(len(rules)):
        rule = rules[rule_i]
        matchedTypeToIndices = {i:[] for i in range(len(rule["target_types"]))}
        # Check all locations to see which locations correspond to which required types by the rule.
        # (note, a rule may correspond to multiple required types but it can only be used in one slot).

        # We obtain a dictionary mapping each required location type to a list of fufilling indices in our location set.
        for location_i in range(len(locations)):
            for rule_targets_i in range(len(rule["target_types"])):
                if isSubtypeOf(rule["target_types"][rule_targets_i], locations[location_i]["type"]):
                    matchedTypeToIndices[rule_targets_i].append(location_i)
        # From the previously described location set, obtain a tuple of indices (if it exists) that satisfies the rule.
        # Do this iteratively, loop over all index sets in construction and add the new index if it isn't already inside.
        print(matchedTypeToIndices)
        rule_indices = []
        for rule_targets_i in range(len(rule["target_types"])):
            atleast_one_satisifying = False
            if len(rule_indices) == 0:
                if len(matchedTypeToIndices[0])>0:
                    rule_indices = [[mtti] for mtti in matchedTypeToIndices[0]]
                    atleast_one_satisifying = True
            else:
                # Every index that can be subbed in at that place.
                for loc_index in matchedTypeToIndices[rule_targets_i]:
                    for pre_i in range(len(rule_indices)):
                        if not loc_index in rule_indices[pre_i]:
                          rule_indices[pre_i].append(loc_index)
                          atleast_one_satisifying = True
            # Prune rules that will never able to be completed to reduce size.
            correct_length_rules = [] 
            for rule_index in rule_indices:
                if len(rule_index) == rule_targets_i+1:
                    correct_length_rules.append(rule_index)
            rule_indices = correct_length_rules

            if not atleast_one_satisifying:
                raise(ValueError(f"Rule {rule_i} has no satisying location for required type index{rule_targets_i}, type {str(rule['target_types'][rule_targets_i])}. Rule will never be trigger - remove rule"))
        filled_rules[rule_i] = rule_indices
    return filled_rules