import numpy as np
import sympy
import json

class Rule:
    def __init__(self, rule_name, targets, reduction = "product"):

        self.rule_name = rule_name

        self.targets = targets
        # Stochiometries/propensities are with respect
        self.stoichiometies = {i:None for i in range(len(targets))}
        self.propensities = {i:None for i in range(len(targets))}
        #self.propensity_types = {i:None for i in range(len(targets))}
        #self.stoichiomety_types = {i:None for i in range(len(targets))}

        self.rule_classes = {i:None for i in range(len(targets))}
        self.stoichiomety_classes = {i:None for i in range(len(targets))}
        self.propensity_classes = {i:None for i in range(len(targets))}

        self.reduction = reduction
        # ADD CHECKING
    
    def addLinearStoichiomety(self, target_indices, stoichiometies, required_target_classes):
        assert(len(target_indices) == len(stoichiometies))
        for i, index in enumerate(target_indices):
            stoichiometry = stoichiometies[i]
            if not self.stoichiometies[index] is None:
                raise(ValueError(f"Overwriting already set stoichiomety is forbidden. Target location {self.targets[index]} at position {str(index+1)}"))
            if isinstance(stoichiometry, (np.ndarray, list)):
                #self.stoichiomety_types[index] = "linear"
                self.stoichiometies[index] = list(stoichiometry)
                self.stoichiomety_classes[index] = required_target_classes[i]
            else:
                raise(ValueError(f"Unrecognised stoichiomety of type {type(stoichiometies[i])}, for target index {index}"))
    def validateFormula(self, formula, required_target_classes):
        # Evaluate when all classes are 0
        subsitution_dict = {}
        for index in range(len(required_target_classes)):
            subsitution_dict[required_target_classes[index]] = 0
        res = formula.evalf(subs=subsitution_dict)
        # We require that a numerical result is outputted and no symbols are left over.
        assert(isinstance(res, (sympy.core.numbers.Float, sympy.core.numbers.Zero)))
        return True
    
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
                #self.propensity_types[index] = "formula"
                # We expect that the array has a single entry.
                sympy_formula = sympy.parse_expr(value)

                self.validateFormula(sympy_formula, required_target_classes[index])
                
            else:
                raise(ValueError(f"Unrecognised propensity function of type {type(values[i])}, for target index {index}"))
            self.propensity_classes[index] = required_target_classes[i]
            self.propensities[index] = value

    def checkRuleDefinition(self):
        for i in range(len(self.targets)):
            if self.stoichiometies[i] is None:
                raise(ValueError(f"The Location type {self.targets[i]} at rule position {str(i+1)} has no defined stochiometry."))
            elif self.propensities[i] is None:
                raise(ValueError(f"The Location type {self.targets[i]} at rule position {str(i+1)} has no defined propensity."))
            #elif self.propensity_types[i] is None:
            #    raise(ValueError(f"The Location type {self.targets[i]} at rule position {str(i+1)} has no defined propensity type."))
            #elif self.stoichiomety_types is None:
            #    raise(ValueError(f"The Location type {self.targets[i]} at rule position {str(i+1)} has no defined stochiometry type."))
        if self.reduction not in ["product", "sum"]:
            raise(ValueError("The only supported reduction opperations are 'product' and 'sum' at the moment"))
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
                     "stoichiometries":self.stoichiometies, "propensities":self.propensities
                     }
        return rule_dict


class Rules:
    def __init__(self):
        self.rules = []

    def addSingleLocationSimpleRule(self, target, propensity, stoichiomety,  
                                    propensity_classes, stoichiomety_classes,
                                    name = "Unnamed single location rule"):
        new_rule = Rule(name, [target])
        new_rule.addLinearStoichiomety(0, [stoichiomety], [stoichiomety_classes])
        new_rule.addSimplePropensityFunction(0, [propensity], [propensity_classes])
        self.rules.append(new_rule)
    
    def addTransportRule(self, source, target, transport_class,
                          propensities, transport_amount, propensity_classes,
                          name = "Unnamed transport rule"):
        assert(len(propensities) == 2)
        assert(len(propensity_classes) == 2)
        new_rule = Rule(name, [source, target])

        source_stochiometry = np.zeros(1)
        source_stochiometry[0] = -transport_amount

        target_stochiometry = np.zeros(1)
        target_stochiometry[0] = transport_amount

        new_rule.addLinearStoichiomety([0, 1], [source_stochiometry, target_stochiometry], [[transport_class], [transport_class]])
        new_rule.addSimplePropensityFunction([0, 1], propensities, propensity_classes)
        self.rules.append(new_rule)

    def addSingleLocationProductionRule(self, target,
                                        reactant_classes, reactant_amount,
                                        product_classes, product_amount,
                                        propensity, propensity_classes,
                                        name = "Unnamed production rule"):
        # Ensure our indices our within bounds

        new_rule = Rule(name, [target])
        reactants_len = len(reactant_classes)
        product_len = len(product_classes)
        assert(len(set(reactant_classes+product_classes)) == reactants_len+product_len)
        target_stochiometry = np.zeros(reactants_len+product_len)

        for i in range(reactants_len):
            target_stochiometry[i] = -reactant_amount[i]

        for i  in range(product_len):
            target_stochiometry[i+reactants_len] = product_amount[i]
        new_rule.addLinearStoichiomety([0], [target_stochiometry], [reactant_classes+product_classes])
        new_rule.addSimplePropensityFunction([0], [propensity], [propensity_classes])
        self.rules.append(new_rule)
    def addOutOfSystemInboundRule(self, target, transport_class, transport_amount,
                                  propensity, propensity_classes, name):
        new_rule = Rule(name, [target])
        target_stochiometry = [transport_amount]
        new_rule.addLinearStoichiomety([0], [target_stochiometry], [transport_class])
        new_rule.addSimplePropensityFunction([0], [propensity], [propensity_classes])
        self.rules.append(new_rule)
    
    #TODO REDO WITHOUT INDEX DEPS
    def writeJSON(self, filename):
        rules_dict = {}
        for i, rule in enumerate(self.rules):
            rule_dict = rule.returnRuleDict()
            rules_dict[i] = rule_dict
        
        json_rules = json.dumps(rules_dict, indent=4, sort_keys=True)

        with open(filename, "w") as outfile:
            outfile.write(json_rules)
        return rules_dict