import numpy as np

class Solver:
    def __init__(self, locations, rules, matched_indices):
        self.locations = locations
        self.rules = rules
        self.matched_indices = matched_indices
        #self.model_state = 
    def simulateOneStep(self):
        raise(TypeError("Abstract class Solver, please use a concrete implementation."))

class GillespieSolver(Solver):
    def __init__(self, locations, rules, matched_indices):
        super().__init__(locations, rules, matched_indices)
    
    def simulateOneStep(self, current_time):
        total_propensity = 0
        propensities = []
        for rule_i in range(len(self.matched_indices)):
            rule = self.rules[rule_i]
            for index_set_I in range(len(self.matched_indices[rule_i])):
                propensity = rule.returnPropensity(np.take(self.locations, self.matched_indices[rule_i][index_set_I]))
                total_propensity+= propensity
                # First element the propensity, second element the rule index, index element pair.
                propensities.append([propensity, [rule_i, index_set_I]])
                
        if total_propensity <= 0:
            print("Finishing model simulation early.\n No rules left to trigger - all rules have 0 propensity.")
            return
        # Generate 0 to 1
        # Random rule
        u1, r2 = np.random.random_sample(2)
        u2 = -np.log(r2)*(1/total_propensity)
        # Random time
        cumulative_prop = 0
        selected_rule = None
        for rule_index, propensity in enumerate(propensities):
            if cumulative_prop+propensity[0] > u1*total_propensity:
                selected_rule = rule_index
                break
            else:
                cumulative_prop += propensity[0]
        selected_rule, selected_locations = propensities[selected_rule][1]
        print(selected_rule)
        assert (self.rules[selected_rule].triggerAttemptedRuleChange(np.take(self.locations, self.matched_indices[selected_rule][selected_locations])))
        return current_time + u2
