import numpy as np
import SupplyChainLocations
import SupplyChainRules
import json



def createLocations():
    all_locations = SupplyChainLocations.Locations()
    all_locations.addSingleChemicalPlant(1,2, "Ammonia")
    all_locations.addSingleChemicalPlant(2,2, "Nitrogen")
    all_locations.writeJSON("Backend/Model Files/BaseLocations.json")

def createRules():
    # Use np.identity(len()) .... for no change
    all_rules = SupplyChainRules.Rules()

    
    # Move Hydrogen from a supplier
    all_rules.addTransportRule(source="NitrogenPlant",target="AmmoniaPlant", 
                               transport_class="H2", propensities=[[1],[1]], transport_amount=2,
                               propensity_classes=[["H2"], ["H2"]], name="Transport Hydrogen")
    
    all_rules.addSingleLocationProductionRule(target="AmmoniaPlant",
                                              reactant_classes=["N2","H2"], reactant_amount=[1,3], 
                                              product_classes=["NH4"],product_amount=[1],propensity=[1,3], 
                                              propensity_classes=["N2", "H2"], name="Test Ammonia Manufacturing")
    all_rules.writeJSON("Backend/Model Files/MetaRules.json")
    # Move Nitrogen from a supplier

    # Produce ammonia 

createLocations()
createRules()

matchRules()


#validateModel()
