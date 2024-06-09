import Rules
import CoreStructures

# We don't require that all locations have the same compartments, only that 

class Model_Backend:

    def __init__(self):
        self.ruleset = None
        self.rules = None
        self.locations = None

        self.ruleset_file = "ruleset.csv"
        self.rules_file = "rules.csv"
        self.locations_file = "locations.csv"

    def load(self):
        self.ruleset = Rules.RulesetLoader().loadRuleset()
        self.rules = Rules.RulesLoader().loadRules()

        self.locations = CoreStructures


if __name__ == "main":
    application = Model_Backend()
    application.load()