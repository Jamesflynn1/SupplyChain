import numpy as np
import sympy
import json

class Rule:
    def __init__(self, rule_name, targets):

        self.rule_name = rule_name

        self.targets = targets
        # Stochiometries/propensities are with respect
        self.stoichiometies = {i:None for i in range(len(targets))}
        self.propensities = {i:None for i in range(len(targets))}

        self.rule_classes = {i:None for i in range(len(targets))}
        self.stoichiomety_classes = {i:None for i in range(len(targets))}
        self.propensity_classes = {i:None for i in range(len(targets))}

    def addLinearStoichiomety(self, target_indices, stoichiometies, required_target_classes):
        assert(len(target_indices) == len(stoichiometies))
        for i, index in enumerate(target_indices):
            stoichiometry = stoichiometies[i]
            if not self.stoichiometies[index] is None:
                raise(ValueError(f"Overwriting already set stoichiomety is forbidden. Target location {self.targets[index]} at position {str(index+1)}"))
            elif isinstance(stoichiometry, (np.ndarray, list)):
                self.stoichiometies[index] = list(stoichiometry)
                self.stoichiomety_classes[index] = required_target_classes[i]
            else:
                raise(ValueError(f"Unrecognised stoichiomety of type {type(stoichiometies[i])}, for target index {index}"))
    
    def addSimplePropensityFunction(self, target_indices, values, required_target_classes):
        # Accepts matrix or constant values at the moment
        assert(len(target_indices) == len(values))
        for i, index in enumerate(target_indices):
            value = values[i]
            print(value)
            if not self.propensities[index] is None:
                raise(ValueError(f"Overwriting already set propensity is forbidden. Target location {self.targets[index]} at position {str(index+1)}"))

            if isinstance(value, str):
                # TODO validate formula here
                # We expect that the array has a single entry.
                sympy_formula = sympy.parse_expr(value)

                self.validateFormula(sympy_formula, required_target_classes[index])
            else:
                raise(ValueError(f"Unrecognised propensity function of type {type(values[i])}, for target index {index}"))
            self.propensity_classes[index] = required_target_classes[i]
            self.propensities[index] = value

    def validateFormula(self, formula, required_target_classes):
        # Evaluate when all classes are 0
        subsitution_dict = {}
        for index in range(len(required_target_classes)):
            subsitution_dict[required_target_classes[index]] = 0
        res = formula.evalf(subs=subsitution_dict)
        # We require that a numerical result is outputted and no symbols are left over.
        assert(isinstance(res, (sympy.core.numbers.Float, sympy.core.numbers.Zero)))
        return True

    def checkRuleDefinition(self):
        for i in range(len(self.targets)):
            if self.stoichiometies[i] is None:
                raise(ValueError(f"The Location type {self.targets[i]} at rule position {str(i+1)} has no defined stochiometry."))
            elif self.propensities[i] is None:
                raise(ValueError(f"The Location type {self.targets[i]} at rule position {str(i+1)} has no defined propensity."))
            
    def mergeClassLists(self):
        # Maps new index to class label
        self.rule_classes = []
        for i, target in enumerate(self.targets):
            sorted_classes = sorted(set(self.propensity_classes[i] + self.stoichiomety_classes[i]))
            tmp_rule_class_dict = {i:comp_class for i, comp_class in enumerate(sorted_classes)}
            # Might be better to remap inputs for more complex functions rather than directly changing the definition of the function.
                # Use additive identity here
            new_stoichiometry = np.zeros(len(sorted_classes))
            for h, old_class in enumerate(self.stoichiomety_classes[i]):
                for j in range(len(tmp_rule_class_dict)):
                    if old_class == tmp_rule_class_dict[j]:
                        new_stoichiometry[j] = self.stoichiometies[i][h]
            self.stoichiometies[i] = list(new_stoichiometry)
            self.rule_classes.append(tmp_rule_class_dict)
        
    def returnRuleDict(self):
        self.checkRuleDefinition()
        self.mergeClassLists()

        # UNPACK DEF TO SPECIFIC LOCATION
        rule_dict = {"name":self.rule_name, "reduction":self.reduction, "target_types":self.targets, "required_classes":self.rule_classes,
                     "stoichiometries":self.stoichiometies, "propensities":self.propensities}
        return rule_dict

class Rules:
    def __init__(self, defined_classes):
        self.rules = []
        self.defined_classes = defined_classes
    
    def addRule(self, rule:Rule):
        if isinstance(rule, Rule):
            self.rules.append(rule)
        else:
            raise(TypeError(f"rule is not a child type of Rule base class (type: {type(rule)})"))
        
    def addRules(self, rules):
        for rule in rules:
            self.addRule(rule)
    
    def checkRulesHaveDefinedClasses(self):
        for rule in self.rules:
            for propensity_class in range(len(rule.propensity_classes)):
                if not propensity_class in self.defined_classes:
                    raise ValueError(f"Class required for the propensity is, {propensity_class} not defined (Rule name: {rule.name})")
            for stoichiometry_class in range(len(rule.stoichiomety_classes)):
                if not stoichiometry_class in self.defined_classes:
                    raise ValueError(f"Class required for the propensity is, {stoichiometry_class} not defined (Rule name: {rule.name})")
        return True


    def writeJSON(self, filename):
        self.checkRulesHaveDefinedClasses()
        rules_dict = {}
        for i, rule in enumerate(self.rules):
            rule_dict = rule.returnRuleDict()
            rules_dict[i] = rule_dict
        
        json_rules = json.dumps(rules_dict, indent=4, sort_keys=True)

        with open(filename, "w") as outfile:
            outfile.write(json_rules)
        return rules_dict