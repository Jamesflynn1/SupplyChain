

from typing import Any

class LocationLoader():
    def __init__(self):

    def loadLocations(self, filepath):
        
class Location:
    def __init__ (self, lat, long, type, compartment_labels, transport_distances, initial_compartment_values):
        self.lat = lat
        self.long = long
        self.type = type
        self.compartment_labels = compartment_labels
        self.transport_distances = transport_distances

        self.compartment_values = initial_compartment_values
