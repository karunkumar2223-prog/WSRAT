from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Resource-Policy",
    "Cross-Origin-Opener-Policy"
]


def analyze_missing_headers(response):

    missing = []
    present = []

    for header in SECURITY_HEADERS:

        if header in response.headers:
            present.append(header)
        else:
            missing.append(header)

    return {
        "present": present,
        "missing": missing
    }


def calculate_header_score(result):

    total = len(SECURITY_HEADERS)

    score = int(
        (len(result["present"]) / total) * 100
    )

    return score


def display_missing_headers(result):

    table = Table(title="Missing Security Headers")

    table.add_column("Header", style="cyan")
    table.add_column("Status", style="green")

    for header in result["present"]:

        table.add_row(header, "Present")

    for header in result["missing"]:

        table.add_row(header, "Missing")

    console.print(table)

    score = calculate_header_score(result)

    console.print(
        Panel.fit(
            f"""
[bold green]Header Score[/bold green]

{score}/100

Present Headers : {len(result['present'])}

Missing Headers : {len(result['missing'])}
""",
            title="Header Summary",
            border_style="green"
        )
    )