import re
import requests

from urllib.parse import urljoin

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

TIMEOUT = 5

def download_js(js_url):

    try:

        r = requests.get(
            js_url,
            timeout=TIMEOUT,
        )

        if r.status_code == 200:

            return r.text

    except Exception:
        pass

    return ""

PATTERNS = {

    "API":

        r'["\'](\/api\/[^"\']+)["\']',

    "JWT":

        r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',

    "AWS":

        r'AKIA[0-9A-Z]{16}',

    "Firebase":

        r'https://[A-Za-z0-9-]+\.firebaseio\.com',

    "GraphQL":

        r'["\'](\/graphql[^"\']*)["\']',

    "WebSocket":

        r'wss?:\/\/[^"\']+',

}


def analyze_javascript(js_files):

    findings = {}

    for js in js_files:

        code = download_js(js)

        if not code:
            continue

        findings[js] = {}

        for name, pattern in PATTERNS.items():

            matches = re.findall(pattern, code)

            findings[js][name] = sorted(set(matches))

    return findings

def calculate_score(findings):

    total = 0

    for js in findings.values():

        for items in js.values():

            total += len(items)

    score = max(100 - total * 5, 0)

    return score

def analyze_js(js_files):

    findings = analyze_javascript(js_files)

    return {

        "findings": findings,

        "score": calculate_score(findings),

    }

def display_js(result):

    table = Table(title="JavaScript Endpoint Analysis")

    table.add_column("JS File")
    table.add_column("Type")
    table.add_column("Count")

    for js, data in result["findings"].items():

        for key, value in data.items():

            table.add_row(
                js,
                key,
                str(len(value))
            )

    console.print(table)

    console.print(
        Panel.fit(
            f"""
JavaScript Score

{result['score']}/100
""",
            title="JavaScript Summary",
        )
    )