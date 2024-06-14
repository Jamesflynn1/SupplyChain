from typing import Any
import numpy as np

class Location:
    def __init__ (self, lat, long, loc_type, label_mapping, transport_distance, initial_class_values):
        self.lat = lat
        self.long = long
        self.loc_type = loc_type
        self.label_mapping = label_mapping
        self.transport_distance = transport_distance

        self.initial_class_values = initial_class_values
        self.class_values = initial_class_values

    
    # Return True if updated successfully, False if negative on update.
    def updateCompartmentValues(self, new_values):
        self.class_values = new_values
    
    def reset(self):
        self.class_values = self.initial_class_values

class Rule:
    def __init__(self, propensity, stoichiometry, rule_name) -> None:
        assert (len(stoichiometry) == len(propensity))
        if isinstance(propensity, (list, np.ndarray)):
            self.propensity_matrix = propensity
            self.propensity_function = lambda x, loc : np.dot(x, self.propensity_matrix[loc])
        else:
            raise(ValueError("Unsupported Propensity in Model Loading"))
        self.rule_name = rule_name
        self.stoichiometry = stoichiometry

    def locationPropensity(self, class_values, location_index):
        return self.propensity_function(class_values, location_index)
    
    def locationAttemptedCompartmentChange(self, class_values, location_index, times_triggered):
        new_values = class_values + times_triggered*self.stoichiometry[location_index]
        return new_values
    
    def returnPropensity(self, locations):
        assert(len(locations) == len(self.stoichiometry))
        # Assume product operation.
        propensity = 1
        for loc_i, location in enumerate(locations):
            propensity *= self.locationPropensity(location.class_values, loc_i)
        assert (propensity >= 0)
        return propensity
    
    # We expect pure Gillespie to have 0 propensity for negative rule changes, however with Tau leaping we may need
    # to check whether a series of rule changes lead 
    def triggerAttemptedRuleChange(self, locations, times_triggered = 1):
        assert(len(locations) == len(self.stoichiometry))
        negative = False
        new_class_values = []
        for loc_i, location in enumerate(locations):
            new_location_values = self.locationAttemptCompartmentChange(location.class_values, loc_i, times_triggered)
            if np.any(new_location_values<0):
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
    def __init__(self) -> None:
        self.timestamps = []
        self.trajectory_location_values = []

    def addEntry(self, time, location_values):
        self.trajectory_location_values.append(location_values)
        self.timestamps.append(time)