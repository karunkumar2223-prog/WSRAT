from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def detect_server(headers):
    return headers.get("Server", "Unknown")


def detect_powered_by(headers):
    return headers.get("X-Powered-By", "Unknown")


def detect_cdn(headers):

    server = headers.get("Server", "").lower()

    if "cloudflare" in server:
        return "Cloudflare"

    if "akamai" in server:
        return "Akamai"

    if "fastly" in server:
        return "Fastly"

    if "cloudfront" in server:
        return "CloudFront"

    if "vercel" in server:
        return "Vercel"

    return "Unknown"


def detect_framework(headers):

    powered = headers.get("X-Powered-By", "").lower()

    if "php" in powered:
        return "PHP"

    if "express" in powered:
        return "Express.js"

    if "asp.net" in powered:
        return "ASP.NET"

    if "django" in powered:
        return "Django"

    if "flask" in powered:
        return "Flask"

    return "Unknown"


def detect_cms(headers):

    powered = headers.get("X-Powered-By", "").lower()

    if "wordpress" in powered:
        return "WordPress"

    if "drupal" in powered:
        return "Drupal"

    if "joomla" in powered:
        return "Joomla"

    return "Unknown"


def analyze_technology(response):

    headers = response.headers

    return {

        "server": detect_server(headers),

        "framework": detect_framework(headers),

        "powered_by": detect_powered_by(headers),

        "cdn": detect_cdn(headers),

        "cms": detect_cms(headers),
    }


def display_technology(result):

    table = Table(title="Technology Fingerprinting")

    table.add_column("Technology", style="cyan")
    table.add_column("Detected", style="green")

    table.add_row("Server", result["server"])
    table.add_row("Framework", result["framework"])
    table.add_row("Powered By", result["powered_by"])
    table.add_row("CDN", result["cdn"])
    table.add_row("CMS", result["cms"])

    console.print(table)

    detected = 0

    for value in result.values():
        if value != "Unknown":
            detected += 1

    score = int((detected / len(result)) * 100)

    console.print(
        Panel.fit(
            f"""
[bold green]Technology Detection Score[/bold green]

{score}/100

Technologies Detected : {detected}
""",
            title="Technology Summary",
            border_style="green"
        )
    )