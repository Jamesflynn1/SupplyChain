import numpy as np
import SupplyChainLocations
import json



def createLocations():
    all_locations = SupplyChainLocations.Locations()
    all_locations.addSingleChemicalPlant(1,2, "Ammonia")
    all_locations.addSingleChemicalPlant(2,2, "Nitrogen")
    all_locations.writeJSON("BaseLocations.json")

##def createRules():
    # Use np.identity(len()) .... for no change

    
    # Move Hydrogen from a supplier


    # Move Nitrogen from a supplier

    # Produce ammonia 

createLocations()