from rich.console import Console
from rich.panel import Panel

console = Console()


class Dashboard:

    @staticmethod
    def grade(score):

        if score >= 95:
            return "A+", "Excellent"

        elif score >= 90:
            return "A", "Very Good"

        elif score >= 80:
            return "B+", "Good"

        elif score >= 70:
            return "B", "Moderate"

        elif score >= 60:
            return "C", "Needs Improvement"

        else:
            return "D", "High Risk"

    @staticmethod
    def show(url, score, modules, duration):

        grade, risk = Dashboard.grade(score)

        console.print(
            Panel.fit(
f"""
Target           : {url}

Scan Duration    : {duration:.2f} sec

Modules Executed : {modules}

Overall Score    : {score}/100

Security Grade   : {grade}

Risk Level       : {risk}
""",
                title="WSRAT Executive Summary",
            )
        )