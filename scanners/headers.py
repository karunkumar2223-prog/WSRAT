from rich.console import Console
from rich.table import Table

console = Console()

SECURITY_HEADERS = {
    "Content-Security-Policy": "Mitigates XSS attacks",
    "Strict-Transport-Security": "Forces HTTPS",
    "X-Frame-Options": "Protects against Clickjacking",
    "X-Content-Type-Options": "Prevents MIME sniffing",
    "Referrer-Policy": "Controls referrer information",
    "Permissions-Policy": "Restricts browser features",
}


def check_security_headers(response):
    results = {}

    for header in SECURITY_HEADERS:
        results[header] = header in response.headers

    score = round((sum(results.values()) / len(results)) * 100)

    return {
        "score": score,
        "headers": results
    }


def display_headers(data):

    headers = data["headers"]

    table = Table(title="HTTP Security Header Analysis")

    table.add_column("Header", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Description")

    for header, description in SECURITY_HEADERS.items():

        if headers[header]:
            status = "[green]✔ Present[/green]"
        else:
            status = "[red]✘ Missing[/red]"

        table.add_row(
            header,
            status,
            description,
        )

    console.print(table)

    console.print(
        f"\n[bold green]Security Score:[/bold green] {data['score']}/100"
    )