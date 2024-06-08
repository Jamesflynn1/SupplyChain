

class Rule:
    def __init__(self, rule_name, targets, reduction = "product"):

        self.rule_name = rule_name

        self.targets = targets
        self.stochiometries = []
        self.propensities = []
        self.propensity_types = {i:"" for i in range(len(targets))}
        self.stochiometry_types = {i:"" for i in range(len(targets))}

        self.reduction = reduction

        # ADD CHECKING
    
    def addLinearStochiometry(self, target_indices, stochometries):


    def addConstantPropensityFunction(self, target_indices, values):

    def addLinearPropensityFunction(self, target_indices, matrices):
