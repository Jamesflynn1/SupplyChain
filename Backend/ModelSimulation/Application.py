import ModelClasses
import ModelSolvers
import ModelLoader

import matplotlib.pyplot as plt

# We don't require that all locations have the same compartments, only that 

class ModelBackend:

    def __init__(self, solver_type = "Gillespie", location_filename = "Locations.json", matched_rules_filename = "LocationMatchedRules.json",
                 model_folder = "Backend/ModelFiles/"):

        self.matched_rules_filename = matched_rules_filename
        self.location_filename = location_filename
        self.model_folder = model_folder
        self.locations = ModelLoader.loadLocations(self.model_folder+self.location_filename)
        self.rules, self.matched_indices = ModelLoader.loadMatchedRules(self.model_folder+self.matched_rules_filename)

        self.simulation_time = 0

        self.trajectory = ModelClasses.Trajectory(self.locations)
        if solver_type == "Gillespie":
            self.solver =  ModelSolvers.GillespieSolver(self.locations, self.rules, self.matched_indices)
        else:
            raise ValueError("Only supported model solver at the moment is exact Gillespie.")

    def resetModel(self):
        for location in self.locations:
            location.reset()
        # Trajectory uses current location values so needs to be defined after location values reset.
        self.trajectory = ModelClasses.Trajectory(self.locations)
        self.simulation_time = 0



    def simulate(self, time_limit, max_iterations = 1000):
        self.resetModel()
        i = 0
        while self.simulation_time < time_limit and i <= max_iterations:
             # Simulate one step should update the location objects automatically with the new compartment values.
             new_time = self.solver.simulateOneStep(self.simulation_time)
             print(new_time)
             self.simulation_time = new_time
             # TODO To save memory - could just add changed location values
             for location_index, location in enumerate(self.locations):
                self.trajectory.addEntry(new_time, location.class_values, location_index)
             i += 1
        return self.trajectory

application = ModelBackend()
out = application.simulate(100)

out.plotClassesOverTime(2, None)
print(out)