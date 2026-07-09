import socket
from urllib.parse import urlparse

import dns.resolver
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def get_domain(url):
    parsed = urlparse(url)

    if parsed.netloc:
        return parsed.netloc

    return parsed.path


def analyze_dns(url):

    domain = get_domain(url)

    records = {}

    record_types = [
        "A",
        "AAAA",
        "MX",
        "NS",
        "TXT",
        "CNAME",
    ]

    for record in record_types:

        try:

            answers = dns.resolver.resolve(domain, record)

            records[record] = [str(answer) for answer in answers]

        except Exception:

            records[record] = []

    try:
        ip = socket.gethostbyname(domain)
    except Exception:
        ip = "Unavailable"

    score = 100

    if not records["MX"]:
        score -= 10

    if not records["TXT"]:
        score -= 10

    if not records["AAAA"]:
        score -= 5

    score = max(score, 0)

    return {
        "domain": domain,
        "ip": ip,
        "records": records,
        "score": score,
    }


def display_dns(result):

    table = Table(title="DNS Intelligence")

    table.add_column("Record")
    table.add_column("Value")

    table.add_row("Domain", result["domain"])
    table.add_row("IP Address", result["ip"])

    for record_type, values in result["records"].items():

        if values:
            table.add_row(record_type, "\n".join(values))
        else:
            table.add_row(record_type, "Not Found")

    console.print(table)

    console.print(
        Panel.fit(
            f"""
DNS Security Score

{result['score']}/100
""",
            title="DNS Summary",
        )
    )