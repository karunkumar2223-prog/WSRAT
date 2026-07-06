import argparse
from urllib import response
import requests

from rich.console import Console
from rich.panel import Panel

from utils.banner import print_banner
from utils.helpers import validate_url
from utils.config import TIMEOUT, USER_AGENT

from scanners.headers import check_security_headers, display_headers
from scanners.ssl import analyze_ssl, display_ssl
from scanners.cookies import analyze_cookies, display_cookies
from scanners.csp import analyze_csp, display_csp
from scanners.http_versions import (
    analyze_http_versions,
    display_http_versions,
)
from scanners.missing_headers import (
    analyze_missing_headers,
    display_missing_headers,
)
from scanners.technology import (
    analyze_technology,
    display_technology,
)
from core.reporter import ReportGenerator

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

def calculate_overall_score(results):

    scores = []

    if "headers" in results:
        scores.append(83)

    if "ssl" in results:
        scores.append(100)

    if "cookies" in results:
        scores.append(85)

    if "csp" in results:
        scores.append(70)

    if "http" in results:
        scores.append(100)

    if "missing_headers" in results:
        scores.append(55)

    if "technology" in results:
        scores.append(20)

    return int(sum(scores)/len(scores))

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

    results = {}

    header_results = check_security_headers(response)

    results["headers"] = header_results

    display_headers(header_results)

    print()

    if args.url.startswith("https://"):
        ssl_result = analyze_ssl(args.url)

        results["ssl"] = ssl_result

        display_ssl(ssl_result)
    else:
     console.print("[yellow]Skipping SSL analysis (HTTP target)[/yellow]")

    print()

    cookies = analyze_cookies(response)

    display_cookies(cookies)

    results["cookies"] = cookies

    print()

    csp = analyze_csp(response)

    display_csp(csp)

    results["csp"] = csp

    console.print("\n[bold green]Security Assessment Completed![/bold green]")

    print()

    http_result = analyze_http_versions(args.url)

    results["http"] = http_result

    display_http_versions(http_result)

    print()

    missing = analyze_missing_headers(response)

    results["missing"] = missing

    display_missing_headers(missing)

    print()

    technology = analyze_technology(response)

    results["technology"] = technology

    display_technology(technology)

    json_report = ReportGenerator.save_json(
        results,
        args.url
)

    html_report = ReportGenerator.save_html(
        results,
        args.url,
        calculate_overall_score(results)
    )

    console.print(f"[green]✔ JSON Report :[/green] {json_report}")
    console.print(f"[green]✔ HTML Report :[/green] {html_report}")

if __name__ == "__main__":
    main()