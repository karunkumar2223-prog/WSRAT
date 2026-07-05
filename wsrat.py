import argparse
import requests
from rich.console import Console
from rich.panel import Panel

from utils.banner import print_banner
from utils.helpers import validate_url
from utils.config import TIMEOUT, USER_AGENT

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

    check_target(args.url)

    console.print("\n[yellow]Starting security assessment...[/yellow]")


if __name__ == "__main__":
    main()