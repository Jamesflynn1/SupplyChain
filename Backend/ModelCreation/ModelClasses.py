import json

class Classes:
    def __init__(self):
        self.class_def_dict = {}
        self.class_names = set([])
    def addClass(self, class_name, class_measurement_unit, class_restriction = "None"):
        if not class_name in self.class_names:
            self.class_def_dict[class_name] = {"class_measurement_unit":class_measurement_unit, "class_restriction":class_restriction}
        else:
            raise(ValueError(f"Duplicate type {class_name} provided."))

    def writeClassJSON(self, filepath):
        
        json_classes = json.dumps(self.class_def_dict, indent=4, sort_keys=True)

        with open(filepath, "w") as outfile:
            outfile.write(json_classes)
        return self.class_def_dict