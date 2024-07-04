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
