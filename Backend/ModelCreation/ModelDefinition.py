import numpy as np

import ModelClasses
import ModelLocations
import ModelRules

import SupplyChainLocations
import SupplyChainRules

import RuleMatching

class ModelDefinition:
    def __init__(self, classes_defintions, create_locations, create_rules, distance_func = SupplyChainLocations.createEuclideanDistanceMatrix, classes_filename = "Classes.json", location_filename = "Locations.json", metarule_filename = "MetaRules.json",
                 matched_rules_filename = "LocationMatchedRules.json", model_folder = "../ModelFiles/"):
        self.classes_filename = classes_filename
        self.location_filename = location_filename
        self.metarule_filename = metarule_filename
        self.matched_rules_filename = matched_rules_filename
        self.model_folder = model_folder

        self.classes_defintions = classes_defintions
        self.create_locations_func = create_locations
        self.create_rules_func = create_rules
        self.distance_func = distance_func

        self.builtin_classes = True

    def createLocations(self):
        all_locations = ModelLocations.Locations(self.defined_classes, self.distance_func)
        locations = self.create_locations_func()
        all_locations.addLocations(locations)
        self.locations = all_locations.writeJSON(f"{self.model_folder}{self.location_filename}")

    def createRules(self):
        # Use np.identity(len()) .... for no change
        all_rules = ModelRules.Rules(self.defined_classes)

        rules = self.create_rules_func()
        all_rules.addRules(rules)

        self.rules = all_rules.writeJSON(f"{self.model_folder}{self.metarule_filename}")

    def defineClasses(self):
        classes = ModelClasses.Classes(self.builtin_classes)
        for class_info in self.classes_defintions:
            classes.addClass(*class_info)
        self.defined_classes = classes.writeClassJSON(f"{self.model_folder}{self.classes_filename}").keys()

    def matchRules(self):
        additional_classes = []
        if self.builtin_classes:
            additional_classes = ModelClasses.Classes().returnBuiltInClasses()
        RuleMatching.writeMatchedRuleJSON(self.rules, self.locations, f"{self.model_folder}{self.matched_rules_filename}", 
                                          additional_classes)
    
    def build(self):
        self.defineClasses()
        self.createLocations()
        self.createRules()
        self.matchRules()


def supplyChainRules():
    transport_nitrogen = SupplyChainRules.TransportRule(source="ChemicalPlant NitrogenPlant",
                                                        target="ChemicalPlant AmmoniaPlant", 
                                                        transport_class="N2", propensities=["1","1"], transport_amount=2,
                                                        propensity_classes=[["N2"], ["N2"]], rule_name="Transport Nitrogen")
    manufacture_ammonia = SupplyChainRules.SingleLocationProductionRule(target="ChemicalPlant AmmoniaPlant",
                                                                        reactant_classes=["N2","H2"], reactant_amount=[1,3], 
                                                                        product_classes=["NH4"],product_amount=[1],propensity="N2*H2",
                                                                        propensity_classes=["N2", "H2"], rule_name="Make Ammonia")
    return [transport_nitrogen, manufacture_ammonia]

def supplyChainLocations():
    ammonia_plant = SupplyChainLocations.ChemicalPlant(1,1,"Example plant")
    nitrogen_plant = SupplyChainLocations.ChemicalPlant(1,1,"Example plant 2")

    ammonia_plant.addAmmoniaManufacturing()
    nitrogen_plant.addNitrogenManufacturing()
    return [ammonia_plant, nitrogen_plant]

#supplyChainClasses = [["NH4", "tonnes"], ["N2", "m^3"], ["H2", "m^3"], ["CH4", "m^3"]]

#model = ModelDefinition(supplyChainClasses, supplyChainLocations, supplyChainRules, model_folder="Backend/ModelFiles/")
#model.build()
