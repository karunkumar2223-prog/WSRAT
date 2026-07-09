import argparse
from tracemalloc import start
import requests
import time

from rich.console import Console
from rich.panel import Panel

from utils.banner import print_banner
from utils.helpers import validate_url
from utils.config import TIMEOUT, USER_AGENT

from core.engine import ScanEngine
from core.reporter import ReportGenerator
from core.scorer import OverallScore

console = Console()


def check_target(url):
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            allow_redirects=True,
        )

        console.print("[green][OK][/green] Target is reachable")
        console.print(f"[cyan]Status Code:[/cyan] {response.status_code}")
        console.print(f"[cyan]Server:[/cyan] {response.headers.get('Server', 'Unknown')}")

        return response

    except requests.exceptions.RequestException as e:
        console.print("[red][✗][/red] Connection failed")
        console.print(e)
        exit()


def main():

    start = time.time()

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
        return

    console.print(
        Panel.fit(
            f"[bold]Target:[/bold] {args.url}",
            title="Assessment",
        )
    )

    response = check_target(args.url)

    # Run all scanners
    engine = ScanEngine(args.url, response)

    results = engine.run()

    # Display scanner results
    engine.display(results)

    # Overall Score
    overall_score = OverallScore.calculate(results)

    console.print(
        Panel.fit(
            f"[bold green]{overall_score}/100[/bold green]",
            title="Overall Security Score",
        )
    )

    # Save Reports
    json_report = ReportGenerator.save_json(
        results,
        args.url,
    )

    html_report = ReportGenerator.save_html(
        results,
        args.url,
        overall_score,
    )


    console.print(f"\n[green]✔ JSON Report:[/green] {json_report}")
    console.print(f"[green]✔ HTML Report:[/green] {html_report}")

    end = time.time()

    duration = end - start

if __name__ == "__main__":
    main()