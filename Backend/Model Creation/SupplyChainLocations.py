import numpy as np
from math import radians, cos, sin, asin, sqrt
import json
# Credit to https://stackoverflow.com/questions/29545704/fast-haversine-approximation-python-pandas

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def createEuclideanDistanceMatrix(lats, longs):
    # Only need to find the upper right triangle.
    distm = np.zeros((len(lats), len(lats)))
    for i in range(len(lats)):
        for h in range(i, len(longs)):
            distm[i][h] = haversine(longs[i], longs[h], lats[i], lats[h])
    # Fill in the lower left triangle
    distm = distm.T+distm
    return distm

# This class is used to create location data in contrast to the model Location class which is used to run the model.
class Location:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.compartment_labels = set([])

    def returnDictDescription(self):
        #For ease of use and to ensure compartment label order is invariant to order construction functions are called 
        ordered_comp_labels = sorted(self.compartment_labels)
        comp_label_mapping = {i:label for i, label in enumerate(ordered_comp_labels)}

        return {"lat" : self.lat, "long":self.long, "label_mapping":comp_label_mapping}
    
# To define a basic model, we need the locations and rules file.
class ChemicalPlant(Location):
    def __init__(self, lat, long):
        super().__init__(lat, long)
        self.added_processing = {"Ammonia" : False, "Nitrogen" : False}
        self.type = "ChemicalPlant"

    def addAmmoniaManufacturing(self):
        if self.added_processing["Ammonia"] == False:
            self.type += " AmmoniaPlant"
            self.compartment_labels.add("NH4")
            self.compartment_labels.add("N2")
            self.compartment_labels.add("H2")
            self.added_processing["Ammonia"] = True
        else:
            raise(ValueError("Already added Ammonia manufacturing"))
    def addNitrogenManufacturing(self):
        if self.added_processing["Nitrogen"] == False:
            self.type += " NitrogenPlant"
            self.compartment_labels.add("CH4")
            self.compartment_labels.add("N2")
            self.added_processing["Nitrogen"] = True
        else:
            raise(ValueError("Already added Nitrogen manufacturing"))
    def returnDictDescription(self, initial_conds=None):
        generic_dict  = super().returnDictDescription()
        values = initial_conds
        if values is None:
            values = np.zeros(len(self.compartment_labels))
        
        generic_dict["initial_values"] = list(values)
        generic_dict["type"] = self.type
        return generic_dict
    
class Farm(Location):
    def __init__(self, lat, long, demand):
        # Sets lat/long and creates and empty set of compartment labels.
        super().__init__(lat, long)
        self.added_crops = {"Wheat" : False, "Barley" : False}
        self.type = "Farm"

    def addWheat(self):
        if self.added_processing["Wheat"] == False:
            self.type += " WheatFarm"
            self.compartment_labels.add("NH4")
            self.compartment_labels.add("Wheat")
            self.added_processing["Wheat"] = True
        else:
            raise(ValueError("Already added Wheat crop"))
        
    def addBarley(self):
        if self.added_processing["Barley"] == False:
            self.type += " BarleyFarm"
            self.compartment_labels.add("NH4")
            self.compartment_labels.add("Barley")
            self.added_processing["Barley"] = True
        else:
            raise(ValueError("Already added Barley crop"))
        
    def returnDictDescription(self, initial_conds=None):
        generic_dict  = super().returnDictDescription()
        values = initial_conds
        if values is None:
            values = np.zeros(len(self.compartment_labels))
        
        generic_dict["initial_values"] = list(values)
        generic_dict["type"] = self.type
        return generic_dict
    

class Locations:
    def __init__(self):
        self.coords =[[],[]]
        self.distanceM = []
        self.locations = []
    
    def writeJSON(self, filename):
        self.coords =  np.array(self.coords)
        distance_matrix =  createEuclideanDistanceMatrix(self.coords[:,0], self.coords[:,1])

        locations_dict = {}

        for i, x in enumerate(self.locations):
            location_dict = x.returnDictDescription()
            location_dict["transport_distance"] = list(distance_matrix[i:].flatten())
            locations_dict[i] = location_dict

        json_locations = json.dumps(locations_dict, indent=4, sort_keys=True)

        with open(filename, "w") as outfile:
            outfile.write(json_locations)

    def addCoordinates(self, lat, long):
        self.coords[0].append(lat)
        self.coords[1].append(long)

    def addSingleChemicalPlant(self, lat, long, type):
        new_plant = ChemicalPlant(lat, long)
        if type == "Ammonia":
            new_plant.addAmmoniaManufacturing()
        elif type == "Nitrogen":
            new_plant.addNitrogenManufacturing()
        self.locations.append(new_plant)
        self.addCoordinates(lat, long)

    def addFarm(self, lat, long):
        new_plant = ChemicalPlant(lat, long)
        if type == "Ammonia":
            new_plant.addAmmoniaManufacturing()
        elif type == "Nitrogen":
            new_plant.addNitrogenManufacturing()
        self.locations.append(new_plant)
        self.addCoordinates(lat, long)