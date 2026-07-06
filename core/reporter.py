import json


class Report:

    @staticmethod
    def save_json(results, filename):

        with open(filename, "w") as f:

            json.dump(results, f, indent=4)