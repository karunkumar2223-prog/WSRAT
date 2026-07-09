import dns.resolver
from urllib.parse import urlparse

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def analyze_subdomains(url):

    domain = urlparse(url).netloc

    discovered = []

    try:
        with open("wordlists/subdomains.txt") as f:
            words = [x.strip() for x in f if x.strip()]
    except FileNotFoundError:
        console.print("[red]Wordlist not found.[/red]")
        return {
            "score": 0,
            "found": []
        }

    resolver = dns.resolver.Resolver()

    for word in words:

        sub = f"{word}.{domain}"

        try:
            resolver.resolve(sub, "A")
            discovered.append(sub)

        except Exception:
            pass

    score = 100

    dangerous = [
        "admin",
        "dev",
        "test",
        "staging",
        "git",
        "jenkins",
    ]

    for sub in discovered:
        for d in dangerous:
            if sub.startswith(d):
                score -= 10

    if score < 0:
        score = 0

    return {
        "found": discovered,
        "score": score
    }


def display_subdomains(result):

    table = Table(title="Subdomain Enumeration")

    table.add_column("Subdomain")
    table.add_column("Status")

    if not result["found"]:

        table.add_row("None Found", "OK")

    else:

        for sub in result["found"]:
            table.add_row(sub, "Resolved")

    console.print(table)

    console.print(
        Panel.fit(
            f"""
Subdomain Score

{result['score']}/100

Discovered : {len(result['found'])}
""",
            title="Subdomain Summary",
        )
    )