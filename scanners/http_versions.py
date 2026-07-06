import httpx

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def analyze_http_versions(url):

    http11 = False
    http2 = False
    http3 = False

    try:

        response = httpx.get(
            url,
            timeout=10,
            http2=True,
            follow_redirects=True
        )

        http11 = True

        if response.http_version == "HTTP/2":
            http2 = True

    except Exception:
        pass

    return {
        "http11": http11,
        "http2": http2,
        "http3": http3
    }


def calculate_protocol_score(result):

    score = 0

    if result["http11"]:
        score += 30

    if result["http2"]:
        score += 70

    return score


def display_http_versions(result):

    table = Table(title="HTTP Protocol Analysis")

    table.add_column("Protocol", style="cyan")
    table.add_column("Supported", style="green")

    table.add_row(
        "HTTP/1.1",
        "Yes" if result["http11"] else "No"
    )

    table.add_row(
        "HTTP/2",
        "Yes" if result["http2"] else "No"
    )

    table.add_row(
        "HTTP/3",
        "Yes" if result["http3"] else "No"
    )

    console.print(table)

    score = calculate_protocol_score(result)

    console.print(
        Panel.fit(
            f"""
[bold green]Protocol Score[/bold green]

{score}/100
""",
            title="HTTP Summary",
            border_style="green"
        )
    )