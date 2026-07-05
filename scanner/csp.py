from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def analyze_csp(response):

    csp = response.headers.get("Content-Security-Policy")

    if not csp:
        return {
            "present": False,
            "policy": "",
            "issues": ["Content-Security-Policy header is missing."]
        }

    issues = []

    if "unsafe-inline" in csp:
        issues.append("Uses unsafe-inline")

    if "unsafe-eval" in csp:
        issues.append("Uses unsafe-eval")

    if "*" in csp:
        issues.append("Wildcard (*) detected")

    if "default-src" not in csp:
        issues.append("Missing default-src")

    if "frame-ancestors" not in csp:
        issues.append("Missing frame-ancestors")

    return {
        "present": True,
        "policy": csp,
        "issues": issues
    }


def display_csp(result):

    table = Table(title="Content Security Policy")

    table.add_column("Check")
    table.add_column("Result")

    table.add_row(
        "Header Present",
        "Yes" if result["present"] else "No"
    )

    if result["present"]:

        if len(result["issues"]) == 0:

            table.add_row(
                "Policy",
                "Looks Secure"
            )

        else:

            for issue in result["issues"]:
                table.add_row("Issue", issue)

    console.print(table)

    score = 100

    score -= len(result["issues"]) * 15

    score = max(score, 0)

    console.print(
        Panel.fit(
            f"""
[bold green]CSP Security Score[/bold green]

{score}/100

Issues Found : {len(result['issues'])}
""",
            title="CSP Summary",
            border_style="green"
        )
    )