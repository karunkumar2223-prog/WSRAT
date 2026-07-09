class OverallScore:

    @staticmethod
    def calculate(results):

        scores = []

        for value in results.values():

            if isinstance(value, dict) and "score" in value:
                scores.append(value["score"])

        if not scores:
            return 0

        return round(sum(scores) / len(scores))