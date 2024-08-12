from typing import Any
import numpy as np
import sympy
import matplotlib.pyplot as plt

class Location:
    def __init__ (self, index, name, lat, long, loc_type, label_mapping, initial_class_values, location_constants):
        self.index = index
        self.name = name
        self.lat = lat
        self.long = long
        self.loc_type = loc_type
        self.label_mapping = label_mapping

        self.initial_class_values = initial_class_values
        self.class_values = initial_class_values
        self.location_constants = location_constants

    
    # Return True if updated successfully, False if negative on update.
    def updateCompartmentValues(self, new_values):
        self.class_values = new_values
    
    def reset(self):
        self.class_values = self.initial_class_values

class Rule:
    def __init__(self, propensity, stoichiometry, rule_name, num_builtin_classes, locations, rule_index_sets) -> None:
        assert (len(stoichiometry) == len(propensity))
        if isinstance(propensity, (list)):
            self.lambda_propensities = []
            self.contains_location_constant = []
            self.sympy_formula = []

            for slot_i, formula_str in enumerate(propensity):
                symbol_string = ''.join([f'x{str(i)} ' for i in range(len(stoichiometry[slot_i])+num_builtin_classes)])
                formula_symbols = sympy.symbols(symbol_string, real=True)

                #symbols = sympy.symbols("".join([f"x{i} " for i in range(len(stoichiometry[loc_i]))]) , real=True)
                #M = sympy.IndexedBase('x', shape=(dim))
            
                #symbols = [f"x{i}" for i in range(len(stoichiometry[loc_i]))]

                if not "loc_" in formula_str:
                    formula = sympy.parse_expr(formula_str)
                    self.sympy_formula.append(formula)
                    f=sympy.lambdify(formula_symbols, formula.simplify(), "numpy")
                    self.contains_location_constant.append(False)
                else:
                    applicable_indices = self.findIndices(rule_index_sets, slot_i)
                    #formula_without_constants = self.subsituteConstants(formula_str, {key:"" for key in list(locations[applicable_indices[0]].location_constants.keys())})

                    f = {loc_index: sympy.lambdify(formula_symbols, sympy.parse_expr(self.subsituteConstants(formula_str, locations[loc_index].location_constants)).simplify(), "numpy") for loc_index in applicable_indices}

                    self.sympy_formula.append(sympy.parse_expr(self.subsituteConstants(formula_str, locations[applicable_indices[0]].location_constants)))

                    self.contains_location_constant.append(True)

                self.lambda_propensities.append(f)
            self.propensity_function = lambda x, loc : np.dot(x, self.propensity_matrix[loc])
        else:
            raise(ValueError("Unsupported Propensity in Model Loading"))
        self.rule_name = rule_name
        self.stoichiometry = stoichiometry
        self.contains_location_constant = np.array(self.contains_location_constant)
    
    def subsituteConstants(self, formula_str:str, location_constants:dict):
        out_formula = formula_str
        for loc_constant in list(location_constants.keys()):
            out_formula = out_formula.replace(loc_constant, str(location_constants[loc_constant]))
        return out_formula

    def findIndices(self, rule_index_sets, slot_index):
        possible_indices = set([])

        for index_set in rule_index_sets:
            possible_indices.add(index_set[slot_index])

        return list(possible_indices)
    def locationAttemptedCompartmentChange(self, class_values, location_index, times_triggered):
        new_values = class_values + times_triggered*self.stoichiometry[location_index]

        return new_values
    
    def returnPropensity(self, locations, builtin_classes):
        assert(len(locations) == len(self.stoichiometry))
        # Assume product operation.
        propensity = 1
        for loc_i, location in enumerate(locations):
            # Apply thresholding here to ensure that no negative propensities are used.
            # print(self.lambda_propensities[loc_i](*location.class_values, *builtin_classes))
            if not self.contains_location_constant[loc_i]:
                propensity *= max(0, self.lambda_propensities[loc_i](*location.class_values, *builtin_classes))
            else:
                propensity *= max(0, self.lambda_propensities[loc_i][location.index](*location.class_values, *builtin_classes))

        assert (propensity >= 0)
        return propensity
    
    # We expect pure Gillespie to have 0 propensity for negative rule changes, however with Tau leaping we may need
    # to check whether a series of rule changes lead 
    def triggerAttemptedRuleChange(self, locations, times_triggered = 1):
        assert(len(locations) == len(self.stoichiometry))
        negative = False
        new_class_values = []
        for loc_i, location in enumerate(locations):
            new_location_values = self.locationAttemptedCompartmentChange(location.class_values, loc_i, times_triggered)
            # CHANGE TODO
            if np.any(new_location_values<-10):
                negative = True
                break
            else:
                new_class_values.append(new_location_values)
        if not negative:
            for loc_i, location in enumerate(locations):
                location.updateCompartmentValues(new_class_values[loc_i])
            return True
        else:

            return False
        
class Trajectory:
    def __init__(self, locations) -> None:
        self.timestamps = {location_index:[0] for location_index, _ in enumerate(locations)}
        self.trajectory_location_values = {location_index:[location.class_values] for location_index, location in enumerate(locations)}

        self.last_time = 0
        self.last_location_index = None

        self.location_labels = {location_index:location.label_mapping for location_index, location in enumerate(locations)}
        self.location_names = {location_index:location.name for location_index, location in enumerate(locations)}

    def addEntry(self, time, location_values, location_index):
        if location_index != self.last_location_index:
            # Add last known time and value 
            self.trajectory_location_values[location_index].append(self.trajectory_location_values[location_index]
                                                                   [len(self.trajectory_location_values[location_index])-1])
            self.timestamps[location_index].append(self.last_time)

        self.trajectory_location_values[location_index].append(location_values)
        self.timestamps[location_index].append(time)

        self.last_time = time
        self.last_location_index = location_index

    def plotAllClassesOverTime(self, location_index):
        # ALLOW NONE AS ENTRY
        class_values = np.array(self.trajectory_location_values[location_index])
        for class_i in range(len(class_values[0])):
            plt.plot(self.timestamps[location_index], class_values[:,class_i])
        plt.legend([self.location_labels[location_index][str(i)].replace("_", " ") for i in range(len(self.location_labels[location_index]))])
        plt.title(f"Classes over time for {self.location_names[location_index]}")
        plt.show()