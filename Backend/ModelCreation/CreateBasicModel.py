import numpy as np
import SupplyChainLocations
import SupplyChainRules
import RuleMatching
import json

class ModelDefinition:
    
    def createLocations(self):
        all_locations = SupplyChainLocations.Locations()
        all_locations.addSingleChemicalPlant(1,2, "Ammonia")
        all_locations.addSingleChemicalPlant(7,4, "Ammonia")

        all_locations.addSingleChemicalPlant(2,2, "Nitrogen")
        all_locations.addSingleChemicalPlant(2,5, "Nitrogen")

        self.locations = all_locations.writeJSON("Backend/ModelFiles/BaseLocations.json")

    def createRules(self):
        # Use np.identity(len()) .... for no change
        all_rules = SupplyChainRules.Rules()

    
        # Move Hydrogen from a supplier
        all_rules.addTransportRule(source="ChemicalPlant NitrogenPlant",target="ChemicalPlant AmmoniaPlant", 
                                   transport_class="H2", propensities=[[1],[1]], transport_amount=2,
                                   propensity_classes=[["H2"], ["H2"]], name="Transport Hydrogen")
    
        all_rules.addSingleLocationProductionRule(target="ChemicalPlant AmmoniaPlant",
                                                  reactant_classes=["N2","H2"], reactant_amount=[1,3], 
                                                  product_classes=["NH4"],product_amount=[1],propensity=[1,3],
                                                  propensity_classes=["N2", "H2"], name="Test Ammonia Manufacturing")
        self.rules = all_rules.writeJSON("Backend/ModelFiles/MetaRules.json")
    def matchRules(self):
        print(RuleMatching.writeMatchedRuleJSON(self.rules, self.locations))

model = ModelDefinition()
model.createLocations()
model.createRules()
model.matchRules()

