import ModelClasses
import ModelState
import ModelSolvers
import ModelLoader

import matplotlib.pyplot as plt

# We don't require that all locations have the same compartments, only that 

class ModelBackend:

    def __init__(self, start_date, solver_type = "Gillespie", location_filename = "Locations.json", matched_rules_filename = "LocationMatchedRules.json", classes_filename = "Classes.json",
                 model_folder = "Backend/ModelFiles/"):

        self.matched_rules_filename = matched_rules_filename
        self.location_filename = location_filename
        self.model_folder = model_folder
        self.classes_dict, self.builtin_classes_dict = ModelLoader.loadClasses(self.model_folder+classes_filename)
        self.locations = ModelLoader.loadLocations(self.model_folder+self.location_filename)
        self.rules, self.matched_indices = ModelLoader.loadMatchedRules(self.model_folder+self.matched_rules_filename, num_builtin_classes=len(self.builtin_classes_dict))

        self.model_state = ModelState.ModelState(self.builtin_classes_dict, start_date)

        self.trajectory = ModelClasses.Trajectory(self.locations)
        if solver_type == "Gillespie":
            self.solver =  ModelSolvers.GillespieSolver(self.locations, self.rules, self.matched_indices, self.model_state)
        else:
            raise ValueError("Only supported model solver at the moment is exact Gillespie.")

    def resetModel(self):
        for location in self.locations:
            location.reset()
        # Trajectory uses current location values so needs to be defined after location values reset.
        self.trajectory = ModelClasses.Trajectory(self.locations)
        self.model_state.reset()



    def simulate(self, time_limit, max_iterations = 1000):
        self.resetModel()
        while self.model_state.elapsed_time < time_limit and self.model_state.iterations <= max_iterations:
             # Simulate one step should update the location objects automatically with the new compartment values.
             new_time = self.solver.simulateOneStep(self.model_state.elapsed_time)
             self.model_state.processUpdate(new_time)
             # TODO To save memory - could just add changed location values
             for location_index, location in enumerate(self.locations):
                self.trajectory.addEntry(new_time, location.class_values, location_index)

             if new_time is None:
                 break
        return self.trajectory

