import ModelClasses
import ModelLoader

# We don't require that all locations have the same compartments, only that 

class Model_Backend:

    def __init__(self, location_filename = "BaseLocations.json", matched_rules_filename = "LocationMatchedRules.json",
                 model_folder = "Backend/ModelFiles/"):
        self.rules = None
        self.matched_indices = None
        self.locations = None

        self.matched_rules_filename = matched_rules_filename
        self.location_filename = location_filename
        self.model_folder = model_folder

    def load(self):
        self.locations = ModelLoader.loadLocations(self.model_folder+self.location_filename)
        self.rules, self.matched_indices = ModelLoader.loadMatchedRules(self.model_folder+self.matched_rules_filename)



print("aaaa")
application = Model_Backend()
application.load()
print("Good")