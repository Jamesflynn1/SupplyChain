

from typing import Any

class LocationLoader():
    def __init__(self):

    def loadLocations(self, filepath):
        
    def validateRulesets(self, ruleset_names):

class Location:
    def __init__ (self, lat, long, ruleset, transport_distances, initial_compartment_values):
        self.lat = lat
        self.long = long

        self.transport_distances = transport_distances

        self.ruleset = ruleset

        self.compartment_sizes = initial_compartment_values

    def returnAllowedRules():
        raise TypeError("Rules not implemented for the parent class, please use the appropriate child class.")

