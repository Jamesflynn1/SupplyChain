import numpy as np
import ModelLocations
from math import radians, cos, sin, asin, sqrt

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
            distm[i][h] = haversine(longs[i], lats[i], longs[h],  lats[h])
    # Fill in the lower left triangle
    distm = distm.T+distm
    return distm

# This class is used to create location data in contrast to the model Location class which is used to run the model.
# To define a basic model, we need the locations and rules file.
class ChemicalPlant(ModelLocations.Location):
    def __init__(self, lat, long, name):
        super().__init__(lat, long, name, loc_type="ChemicalPlant")
        self.added_processing = {"Ammonia" : False, "Nitrogen" : False}

    def addAmmoniaManufacturing(self):
        if self.added_processing["Ammonia"] == False:
            self.loc_type += " AmmoniaPlant"
            self.class_labels.add("NH4")
            self.class_labels.add("N2")
            self.class_labels.add("H2")
            self.added_processing["Ammonia"] = True
        else:
            raise(ValueError("Already added Ammonia manufacturing"))
    def addNitrogenManufacturing(self):
        if self.added_processing["Nitrogen"] == False:
            self.loc_type += " NitrogenPlant"
            self.class_labels.add("CH4")
            self.class_labels.add("N2")
            self.added_processing["Nitrogen"] = True
        else:
            raise(ValueError("Already added Nitrogen manufacturing"))
    
class FarmRegion(ModelLocations.Location):
    def __init__(self, lat, long, name):
        # Sets lat/long and creates and empty set of compartment labels.
        super().__init__(lat, long, name, loc_type="FarmRegion")

        crops = ["Cereals", "Wheat", "Barley"]
        for crop in crops:
            self.class_labels.add(crop)