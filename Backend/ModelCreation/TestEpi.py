import numpy as np

import ModelDefinition
import ModelLocations

import SupplyChainLocations
import SupplyChainRules
import json

epiClasses = [["S", "people"], ["E", "people"], ["I", "people"], ["R", "people"]]

model_constants = {
    "Exposure_rate":0.11,
    "Infection_rate":0.2,
    "Recovery_rate":0.3,
    "Death_proportion":0.01
}

def epidemologyRules():
    # Frequency vs prevalance - /N but can also use a frequency propensity (fits some dieases better than others).
    exposure = SupplyChainRules.SingleLocationProductionRule("Region", ["S"], [1], ["E"], [1], 
                                                              f"{model_constants["Exposure_rate"]}*I*S/(S+E+I+R)",
                                                              ["S","E","I","R"], "Exposure")
    infection = SupplyChainRules.SingleLocationProductionRule("Region", ["E"], [1], ["I"], [1], 
                                                              f"{model_constants["Infection_rate"]}*E",
                                                              ["E"], "Infection")    
    recovery = SupplyChainRules.SingleLocationProductionRule("Region", ["I"], [1], ["R"], [1], 
                                                            f"{model_constants["Recovery_rate"]}*I",
                                                            ["I"], "Recovery")
    death = SupplyChainRules.ExitEntranceRule("Region", "I", 1, 
                                              f"{model_constants["Death_proportion"]}*{model_constants["Recovery_rate"]}*I", ["I"], "Death")
    return [exposure, infection, recovery, death]

class Region (ModelLocations.Location):
    def __init__(self, lat, long, name):
        # Sets lat/long and creates and empty set of compartment labels.
        super().__init__(lat, long, name, loc_type="Region")
        self.class_labels.add("S")
        self.class_labels.add("E")
        self.class_labels.add("I")
        self.class_labels.add("R")

def sirLocations():
    all_locations = []
    # Midpoints from wikipedia, South East and London uses South East midpoint (combined to match DEFRA reporting)
    region_infos = [[55, -1.87, "North East"], [55, -1.87, "North West"], [53.566667, -1.2, "Yorkshire & The Humber"], [52.98, -0.75, "East Midlands"], [52.478861, -2.256306, "West Midlands"], 
                    [52.24, 0.41, "East of England"], [51.515447, -0.09214, "London"], [51.3, -0.8, "South East"], [50.96, -3.22, "South West"], [56.816738, -4.183963, "Scotland"], 
                    [52.33022, -3.766409,"Wales"]]
    # ONS mid 2022 estimates
    region_populations = [2683040, 7516113, 5541262, 4934939, 6021653, 6398497, 8866180, 9379833, 5764881, 5447700, 3131640]

    for region_index, region_info in enumerate(region_infos):
        region = Region(*region_info)
        region.setInitialConditions({"S":region_populations[region_index], "I":3})
        all_locations.append(region)

    return all_locations

model = ModelDefinition.ModelDefinition(epiClasses, sirLocations, epidemologyRules, model_folder="Backend/ModelCreation/")
model.build()