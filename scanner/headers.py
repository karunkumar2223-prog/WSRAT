from rich.console import Console
from rich.table import Table

console = Console()

SECURITY_HEADERS = {
    "Content-Security-Policy": "Mitigates XSS attacks",
    "Strict-Transport-Security": "Forces HTTPS",
    "X-Frame-Options": "Protects against Clickjacking",
    "X-Content-Type-Options": "Prevents MIME sniffing",
    "Referrer-Policy": "Controls referrer information",
    "Permissions-Policy": "Restricts browser features"
}


def check_security_headers(response):
    """
    Check for important HTTP security headers.
    Returns:
        dict(header -> bool)
    """
    results = {}

    for header in SECURITY_HEADERS:
        results[header] = header in response.headers

    return results


def display_headers(results):
    table = Table(title="HTTP Security Header Analysis")

    table.add_column("Header", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center")
    table.add_column("Description", style="green")

    score = 0

    for header, description in SECURITY_HEADERS.items():

        if results[header]:
            status = "[green]✔ Present[/green]"
            score += 1
        else:
            status = "[red]✘ Missing[/red]"

        table.add_row(header, status, description)

    console.print(table)

    console.print(
        f"\n[bold cyan]Security Score:[/bold cyan] {score}/{len(SECURITY_HEADERS)}"
    )

    return score