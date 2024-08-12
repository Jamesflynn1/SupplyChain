import ModelClasses
import ModelState
import ModelSolvers
import ModelLoader

import RuleChain

import matplotlib.pyplot as plt
import time
# We don't require that all locations have the same compartments, only that 

class ModelBackend:

    def __init__(self, start_date, solver_type:str = "Gillespie", location_filename:str = "Locations.json", matched_rules_filename:str = "LocationMatchedRules.json", classes_filename:str = "Classes.json",
                 model_folder:str = "Backend/ModelFiles/", propensity_caching:bool = True):

        self.matched_rules_filename = matched_rules_filename
        self.location_filename = location_filename
        self.model_folder = model_folder
        self.classes_dict, self.builtin_classes_dict = ModelLoader.loadClasses(self.model_folder+classes_filename)
        self.locations = ModelLoader.loadLocations(self.model_folder+self.location_filename)
        self.rules, self.matched_indices = ModelLoader.loadMatchedRules(self.model_folder+self.matched_rules_filename, self.locations, num_builtin_classes=len(self.builtin_classes_dict))

        self.model_state = ModelState.ModelState(self.builtin_classes_dict, start_date)

        self.trajectory = ModelClasses.Trajectory(self.locations)

        if propensity_caching:
            self.rule_propensity_update_dict = RuleChain.returnOneStepRuleUpdates(self.rules, self.locations, self.matched_indices, self.model_state.returnModelClasses())
        else:
            self.rule_propensity_update_dict = {}

        if solver_type == "Gillespie":
            self.solver =  ModelSolvers.GillespieSolver(self.locations, self.rules, self.matched_indices, self.model_state, propensity_caching, self.rule_propensity_update_dict)
        else:
            raise ValueError("Only supported model solver at the moment is exact Gillespie.")

    def resetModel(self):
        for location in self.locations:
            location.reset()
        # Trajectory uses current location values so needs to be defined after location values reset.
        self.trajectory = ModelClasses.Trajectory(self.locations)
        self.model_state.reset()
        self.solver.reset()

    def simulate(self, time_limit, max_iterations:int = 1000):
        self.resetModel()
        start_perf_time = time.perf_counter()
        while self.model_state.elapsed_time < time_limit and self.model_state.iterations < max_iterations:
             # Simulate one step should update the location objects automatically with the new compartment values.
             new_time = self.solver.simulateOneStep(self.model_state.elapsed_time)
             self.model_state.processUpdate(new_time)
             # TODO To save memory - could just add changed location values
             for location_index, location in enumerate(self.locations):
                self.trajectory.addEntry(new_time, location.class_values, location_index)

             if new_time is None:
                 break
        end_perf_time = time.perf_counter()
        print(f"The simulation has finished after {self.model_state.elapsed_time} {self.model_state.time_measurement}, requiring {self.model_state.iterations} iterations and {end_perf_time-start_perf_time} secs of compute time")
        return self.trajectory

