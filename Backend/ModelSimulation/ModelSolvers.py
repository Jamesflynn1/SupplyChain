import numpy as np

class Solver:
    def __init__(self, locations, rules, matched_indices):
        self.locations = locations
        self.rules = rules
        self.matched_indices = matched_indices
    def simulateOneStep(self):
        raise(TypeError("Abstract class Solver, please use a concrete implementation."))

class GillespieSolver:
    def __init__(self, locations, rules, matched_indices):
        super().__init__(locations, rules, matched_indices)
    
    def simulateOneStep(self, current_time):
        total_propensity = 0
        for rule_i in range(self.matched_indices):
            rule = self.rules[rule_i]
            for index_set_I in range(self.matched_indices[rule_i]):
                total_propensity+= rule.returnPropensity(np.take(self.locations, self.matched_indices[rule_i][index_set_I]))

        # Generate 0 to 1
        # Random rule
        u1, r2 = np.random.random_sample(2)
        u2 = 
        # Random time
        
        return current_time

        