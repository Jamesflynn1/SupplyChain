import ModelClasses
import ModelSolvers
import ModelLoader

# We don't require that all locations have the same compartments, only that 

class ModelBackend:

    def __init__(self, solver_type = "Gillespie", location_filename = "BaseLocations.json", matched_rules_filename = "LocationMatchedRules.json",
                 model_folder = "Backend/ModelFiles/"):

        self.matched_rules_filename = matched_rules_filename
        self.location_filename = location_filename
        self.model_folder = model_folder
        self.locations = ModelLoader.loadLocations(self.model_folder+self.location_filename)
        self.rules, self.matched_indices = ModelLoader.loadMatchedRules(self.model_folder+self.matched_rules_filename)

        self.trajectory = ModelClasses.Trajectory()
        if solver_type == "Gillespie":
            self.solver =  ModelSolvers.GillespieSolver(self.locations, self.rules, self.matched_indices)
        else:
            raise ValueError("Only supported model solver at the moment is exact Gillespie.")

    def resetModel(self):
        self.trajectory = ModelClasses.Trajectory()
        for location in self.locations:
            location.reset()


    def simulate(self, time_steps):
        self.resetModel()
        for iterations in range(time_steps):
             # Simulate one step should update the location objects automatically with the new compartment values.
             new_time = self.solver.simulateOneStep(self.simulation_time)
             location_values = []
             for location in self.locations:
                 location_values.append(location.class_values)
             self.trajectory.addEntry(new_time, location_values)
        return self.trajectory

application = ModelBackend()
