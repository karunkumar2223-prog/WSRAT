import socket
import ssl
from urllib.parse import urlparse
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def analyze_ssl(url):
    """
    Analyze SSL/TLS certificate information.
    """

    parsed = urlparse(url)
    hostname = parsed.hostname
    port = 443

    context = ssl.create_default_context()

    try:
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:

                cert = secure_sock.getpeercert()
                tls_version = secure_sock.version()

        issuer = dict(x[0] for x in cert["issuer"])
        subject = dict(x[0] for x in cert["subject"])

        issued_to = subject.get("commonName", "Unknown")
        issued_by = issuer.get("commonName", "Unknown")

        valid_from = datetime.strptime(
            cert["notBefore"],
            "%b %d %H:%M:%S %Y %Z"
        )

        valid_until = datetime.strptime(
            cert["notAfter"],
            "%b %d %H:%M:%S %Y %Z"
        )

        remaining_days = (valid_until - datetime.utcnow()).days

        certificate_lifetime = (
            valid_until - valid_from
        ).days

        expired = remaining_days < 0

        weak_tls = tls_version in [
            "TLSv1",
            "TLSv1.1"
        ]

        return {
            "issued_to": issued_to,
            "issued_by": issued_by,
            "valid_from": valid_from.strftime("%Y-%m-%d"),
            "valid_until": valid_until.strftime("%Y-%m-%d"),
            "remaining_days": remaining_days,
            "certificate_lifetime": certificate_lifetime,
            "expired": expired,
            "tls_version": tls_version,
            "weak_tls": weak_tls,
        }

    except Exception as e:
        console.print(f"[red]SSL Error:[/red] {e}")
        return None


def calculate_ssl_score(result):
    """
    Calculate SSL Security Score.
    """

    score = 100

    if result["expired"]:
        score -= 50

    if result["remaining_days"] < 30:
        score -= 20

    if result["weak_tls"]:
        score -= 30

    return max(score, 0)


def display_ssl(result):
    """
    Display SSL analysis.
    """

    if result is None:
        return

    table = Table(title="SSL/TLS Certificate Analysis")

    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    table.add_row("Issued To", result["issued_to"])
    table.add_row("Issued By", result["issued_by"])
    table.add_row("Valid From", result["valid_from"])
    table.add_row("Valid Until", result["valid_until"])
    table.add_row("Days Remaining", str(result["remaining_days"]))
    table.add_row(
        "Certificate Lifetime",
        f"{result['certificate_lifetime']} Days"
    )
    table.add_row(
        "Expired",
        "Yes" if result["expired"] else "No"
    )
    table.add_row(
        "TLS Version",
        result["tls_version"]
    )
    table.add_row(
        "Weak TLS",
        "Yes" if result["weak_tls"] else "No"
    )

    console.print(table)

    # -----------------------------
    # Certificate Health
    # -----------------------------

    if result["expired"]:
        console.print(
            "[bold red]❌ Certificate has expired![/bold red]"
        )

    elif result["remaining_days"] < 30:
        console.print(
            "[bold yellow]⚠ Certificate expires soon.[/bold yellow]"
        )

    else:
        console.print(
            "[bold green]✅ Certificate is healthy.[/bold green]"
        )

    # -----------------------------
    # SSL Score
    # -----------------------------

    score = calculate_ssl_score(result)

    console.print()

    console.print(
        Panel.fit(
            f"""
[bold green]SSL Security Score[/bold green]

[bold cyan]{score}/100[/bold cyan]

TLS Version : {result['tls_version']}

Certificate Lifetime : {result['certificate_lifetime']} Days

Days Remaining : {result['remaining_days']} Days
""",
            title="SSL Summary",
            border_style="green"
        )
    )