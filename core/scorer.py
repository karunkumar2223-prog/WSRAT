class SecurityScore:

    def __init__(self):

        self.modules = {}

    def add(self, module, score):

        self.modules[module] = score

    def overall(self):

        if len(self.modules) == 0:

            return 0

        return int(sum(self.modules.values()) / len(self.modules))

    def risk(self):

        score = self.overall()

        if score >= 90:
            return "LOW"

        elif score >= 75:
            return "MEDIUM"

        elif score >= 50:
            return "HIGH"

        return "CRITICAL"