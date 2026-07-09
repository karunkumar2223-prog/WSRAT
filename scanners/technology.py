import requests

from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def analyze_technology(response):

    headers = response.headers
    html = response.text.lower()

    result = {
        "server": headers.get("Server", "Unknown"),
        "framework": "Unknown",
        "powered_by": headers.get("X-Powered-By", "Unknown"),
        "cdn": "Unknown",
        "cms": "Unknown",
        "frontend": [],
        "security": [],
        "compression": headers.get("Content-Encoding", "None"),
        "cache": headers.get("X-Cache", "Unknown"),
    }

    server = headers.get("Server", "").lower()

    if "nginx" in server:
        result["server"] = "Nginx"

    elif "apache" in server:
        result["server"] = "Apache"

    elif "iis" in server:
        result["server"] = "Microsoft IIS"

    elif "caddy" in server:
        result["server"] = "Caddy"

    if "fastly" in headers.get("Via", "").lower():
        result["cdn"] = "Fastly"

    elif "cloudflare" in headers.get("Server", "").lower():
        result["cdn"] = "Cloudflare"

    elif "akamai" in str(headers).lower():
        result["cdn"] = "Akamai"

    if "wordpress" in html:
        result["cms"] = "WordPress"

    elif "drupal" in html:
        result["cms"] = "Drupal"

    elif "joomla" in html:
        result["cms"] = "Joomla"

    if "react" in html:
        result["frontend"].append("React")

    if "_next" in html:
        result["frontend"].append("Next.js")

    if "vue" in html:
        result["frontend"].append("Vue")

    if "angular" in html:
        result["frontend"].append("Angular")

    if "strict-transport-security" in headers:
        result["security"].append("HSTS")

    if "content-security-policy" in headers:
        result["security"].append("CSP")

    detected = 0

    for key in [
        "server",
        "framework",
        "powered_by",
        "cdn",
        "cms",
    ]:
        if result[key] != "Unknown":
            detected += 1

    detected += len(result["frontend"])
    detected += len(result["security"])

    result["score"] = min(detected * 15, 100)

    return result


def display_technology(result):

    table = Table(title="Technology Fingerprinting")

    table.add_column("Property")
    table.add_column("Value")

    table.add_row("Server", result["server"])
    table.add_row("Framework", result["framework"])
    table.add_row("Powered By", result["powered_by"])
    table.add_row("CDN", result["cdn"])
    table.add_row("CMS", result["cms"])
    table.add_row(
        "Frontend",
        ", ".join(result["frontend"]) if result["frontend"] else "Unknown",
    )
    table.add_row(
        "Security",
        ", ".join(result["security"]) if result["security"] else "None",
    )
    table.add_row("Compression", result["compression"])
    table.add_row("Cache", result["cache"])

    console.print(table)

    console.print(
        Panel.fit(
            f"""
Technology Score

{result['score']}/100
""",
            title="Technology Summary",
        )
    )