import csv

class RulesetLoader():
    def __init__(self):
        self.rulesets = {}
    def loadRuleset(self, filepath, ruleset_name):
        ruleset_names = set()
        with open('filepath', newline='') as rulessetcsv:
            for i, row in enumerate(rulessetcsv):
                self.rulesets[row[0]] = row[1:]
                ruleset_names.add(row[0])
                if ruleset_names.__contains__(row[0]):
                    raise(ValueError(f"Duplicate Ruleset name, {row[0]}, on line {str(i)}"))
        return self.rulesets
    
    def validateRules(self, rule_names):
        for ruleset_name in list(self.rulesets.keys()):
            for rule_name in self.rulesets[ruleset_name]:
              if not rule_name in rule_names:
                  raise(ValueError(f"Ruleset Contains Rule {rule_name} with no definition found."))



class RulesLoader():
    def __init__(self):

    def loadRules (self, filepath):

class Ruleset:
    def __init__(self, ruleset):
        self.rulesets = ruleset

class Rule:
    def __init__ (self, stoichiometry, propensity_function, target_stoichiometry = None, targets = None):
        self.stoichiometry = stoichiometry
        self.target_stoichiometry = target_stoichiometry
        self.propensity_function = propensity_function
        self.targets = targets
        if not ((targets is None and target_stoichiometry is None) or
            not (targets is None) and not(target_stoichiometry is None)):
            if targets is None:
                raise(ValueError("Define list of valid rule targets or remove target stoichiometry"))
            else:
                raise(ValueError("Define valid target stoichiometry or list of valid rule targets"))
        if len(targets) != len(target_stoichiometry):
            raise(ValueError("Number of target stoichiometries must match the number of targets."))
   

    def returnPropensity(self, compartment_values, targets_compartment_values = None):
        return self.propensity_function(compartment_values, targets_compartment_values)
    
    #TODO write to return source and target
    def returnCompartmentChanges(self, compartment_values, targets_compartment_values = None):
        return self.stoichiometry @ compartment_values
    
    # APPLY the rule to the targets in the same order as they passed to the function here
    # Note the only only distinction of source and target is that the source location is where the rule is triggered.
    def applyRule(self, source_location, target_locations = None):
        if not self.targets is None:
            self.validateTargets()
        value_change = self.returnCompartmentChanges()
        source_location.add(value_change[0])

    def validateTargets(self, target_locations):
        """" Ensures that the locations that will be targeted (other than the source)
        
        """
        assert(len(target_locations) == len(self.targets))
        for i, location in enumerate(target_locations):
            if not self.targets[i].__contains__(location.type):
                raise(ValueError(f"Expected location to have types '{self.targets[i]}', instead found location of type '{location.type}'"))