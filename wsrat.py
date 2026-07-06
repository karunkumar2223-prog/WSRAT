import argparse
from urllib import response
import requests
from rich.console import Console
from rich.panel import Panel

from scanner import cookies
from utils.banner import print_banner
from utils.helpers import validate_url
from utils.config import TIMEOUT, USER_AGENT
from scanner.headers import check_security_headers, display_headers
from scanner.ssl_checker import analyze_ssl, display_ssl
from scanner.cookies import analyze_cookies, display_cookies
from scanner.csp import analyze_csp, display_csp
from scanner.http_versions import (analyze_http_versions,display_http_versions,)
from scanner.missing_headers import (analyze_missing_headers,display_missing_headers,)
from scanner.tech import (analyze_technology,display_technology,)
console = Console()


def check_target(url):
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            allow_redirects=True,
        )

        console.print("[green][✓][/green] Target is reachable")
        console.print(f"[cyan]Status Code:[/cyan] {response.status_code}")
        console.print(f"[cyan]Server:[/cyan] {response.headers.get('Server', 'Unknown')}")

        return response

    except requests.exceptions.RequestException as e:
        console.print(f"[red][✗][/red] Connection failed")
        console.print(e)
        exit()


def main():
    parser = argparse.ArgumentParser(
        description="Web Security Recon & Assessment Toolkit"
    )

    parser.add_argument(
        "url",
        help="Target URL",
    )

    args = parser.parse_args()

    print_banner()

    if not validate_url(args.url):
        console.print("[red]Invalid URL[/red]")
        exit()

    console.print(
        Panel.fit(
            f"[bold]Target:[/bold] {args.url}",
            title="Assessment",
        )
    )

    response = check_target(args.url)

    results = check_security_headers(response)
    display_headers(results)

    print()

    if args.url.startswith("https://"):
        ssl_result = analyze_ssl(args.url)
        display_ssl(ssl_result)
    else:
     console.print("[yellow]Skipping SSL analysis (HTTP target)[/yellow]")

    print()

# -----------------------------
# Cookie Security Analysis
# -----------------------------
    cookies = analyze_cookies(response)
    display_cookies(cookies)

# -----------------------------
# CSP Analysis
# -----------------------------
    print()

    csp = analyze_csp(response)

    display_csp(csp)

    console.print("\n[bold green]Security Assessment Completed![/bold green]")

# -----------------------------
# HTTP Versions Analysis
# -----------------------------
    print()

    versions = analyze_http_versions(args.url)

    display_http_versions(versions)

    print()

    missing = analyze_missing_headers(response)

    display_missing_headers(missing)

    print()

    technology = analyze_technology(response)

    display_technology(technology)


if __name__ == "__main__":
    main()