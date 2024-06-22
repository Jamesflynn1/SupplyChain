import numpy as np

import json

class Location:
    def __init__(self, lat, long, name, loc_type):
        self.lat = lat
        self.long = long
        self.name = name
        self.class_labels = set([])
        self.loc_type = loc_type
        
    def returnDictDescription(self, initial_conds=None):
        #For ease of use and to ensure compartment label order is invariant to order construction functions are called.
        ordered_class_labels = sorted(self.class_labels)
        class_label_mapping = {i:label for i, label in enumerate(ordered_class_labels)}
        if initial_conds is None:
            initial_conds = list(np.zeros(len(self.class_labels)))
        return {"lat" : self.lat, "long":self.long, "label_mapping":class_label_mapping, "type":self.loc_type, "initial_values":initial_conds}
    

class Locations:
    def __init__(self, defined_classes, distance_function):
        self.coords =[[],[]]
        self.locations = []
        self.defined_classes = defined_classes
        self.distance_function = distance_function
        
    def checkLocationClassesDefined(self):
        for location in self.locations:
            for location_class_label in location.class_labels:
                if not location_class_label in self.defined_classes:
                    raise ValueError(f"Class {location_class_label} not defined (Location name: {location.name})")
        return True
    
    def writeJSON(self, filename):
        self.checkLocationClassesDefined()
        self.coords =  np.array(self.coords)
        distance_matrix =  self.distance_function(self.coords[0,:], self.coords[1,:])

        locations_dict = {}

        for i, x in enumerate(self.locations):
            location_dict = x.returnDictDescription()
            location_dict["transport_distance"] = list(distance_matrix[i,:].flatten())
            locations_dict[i] = location_dict

        json_locations = json.dumps(locations_dict, indent=4, sort_keys=True)

        with open(filename, "w") as outfile:
            outfile.write(json_locations)
        return locations_dict
    
    def addCoordinates(self, lat, long):
        self.coords[0].append(lat)
        self.coords[1].append(long)

    def addLocation(self, location:Location):
        if isinstance(location, Location):
            self.locations.append(location)
            self.addCoordinates(location.lat, location.long)
        else:
            raise(TypeError(f"location is not a child type of Location base class (type: {type(location)})"))
    def addLocations(self, locations):
        for location in locations:
            self.addLocation(location)