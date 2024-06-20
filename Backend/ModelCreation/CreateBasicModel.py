import numpy as np
import SupplyChainLocations
import SupplyChainRules
import RuleMatching
import json

class ModelDefinition:
    def __init__(self, location_filename = "Locations.json", metarule_filename = "MetaRules.json",
                 matched_rules_filename = "LocationMatchedRules.json", model_folder = "Backend/ModelFiles/"):
        self.location_filename = location_filename
        self.metarule_filename = metarule_filename
        self.matched_rules_filename = matched_rules_filename
        self.model_folder = model_folder

    def createLocations(self):
        all_locations = SupplyChainLocations.Locations()
        all_locations.addSingleChemicalPlant(1,2, "Ammonia")
        all_locations.addSingleChemicalPlant(7,4, "Ammonia")

        all_locations.addSingleChemicalPlant(2,2, "Nitrogen")
        all_locations.addSingleChemicalPlant(2,5, "Nitrogen")

        self.locations = all_locations.writeJSON(f"{self.model_folder}{self.location_filename}")

    def createRules(self):
        # Use np.identity(len()) .... for no change
        all_rules = SupplyChainRules.Rules()

    
        # Move Hydrogen from a supplier
        all_rules.addTransportRule(source="ChemicalPlant NitrogenPlant",target="ChemicalPlant AmmoniaPlant", 
                                   transport_class="N2", propensities=["1","1"], transport_amount=2,
                                   propensity_classes=[["N2"], ["N2"]], name="Transport Nitrogen")

        all_rules.addSingleLocationProductionRule(target="ChemicalPlant AmmoniaPlant",
                                                  reactant_classes=["N2","H2"], reactant_amount=[1,3], 
                                                  product_classes=["NH4"],product_amount=[1],propensity="N2*H2",
                                                  propensity_classes=["N2", "H2"], name="Test Ammonia Manufacturing")      
          
        self.rules = all_rules.writeJSON(f"{self.model_folder}{self.metarule_filename}")

    def matchRules(self):
        RuleMatching.writeMatchedRuleJSON(self.rules, self.locations, f"{self.model_folder}{self.matched_rules_filename}")
    
    def build(self):
        model.createLocations()
        model.createRules()
        model.matchRules()

model = ModelDefinition()
model.build()

