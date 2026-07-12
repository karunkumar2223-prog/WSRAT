import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

TIMEOUT = 5


def analyze_crawler(url):

    pages = []
    javascript = []
    apis = []

    try:

        r = requests.get(url, timeout=TIMEOUT)

        soup = BeautifulSoup(r.text, "html.parser")

        domain = urlparse(url).netloc

        # ------------------------
        # Links
        # ------------------------

        for tag in soup.find_all("a", href=True):

            href = urljoin(url, tag["href"])

            if urlparse(href).netloc == domain:

                if href not in pages:
                    pages.append(href)

        # ------------------------
        # JavaScript Files
        # ------------------------

        for tag in soup.find_all("script", src=True):

            src = urljoin(url, tag["src"])

            if src not in javascript:
                javascript.append(src)

        # ------------------------
        # API Endpoints
        # ------------------------

        keywords = [
            "/api/",
            "/graphql",
            "/v1/",
            "/v2/",
            "/rest/",
        ]

        for page in pages:

            for keyword in keywords:

                if keyword.lower() in page.lower():

                    apis.append(page)

        apis = list(set(apis))

        score = 100

        if len(javascript) > 10:
            score -= 10

        if len(apis) > 5:
            score -= 10

        return {
            "pages": pages,
            "javascript": javascript,
            "apis": apis,
            "score": max(score, 0)
        }

    except Exception:

        return {
            "pages": [],
            "javascript": [],
            "apis": [],
            "score": 0
        }


def display_crawler(result):

    table = Table(title="HTML Crawling")

    table.add_column("Category")
    table.add_column("Count")

    table.add_row("Pages", str(len(result["pages"])))
    table.add_row("JavaScript", str(len(result["javascript"])))
    table.add_row("API Endpoints", str(len(result["apis"])))

    console.print(table)

    if result["javascript"]:

        js_table = Table(title="JavaScript Files")

        js_table.add_column("URL")

        for js in result["javascript"][:10]:

            js_table.add_row(js)

        console.print(js_table)

    if result["apis"]:

        api_table = Table(title="Discovered API Endpoints")

        api_table.add_column("Endpoint")

        for api in result["apis"]:

            api_table.add_row(api)

        console.print(api_table)

    console.print(
        Panel.fit(
            f"""
Crawler Score : {result['score']}/100

Pages Found : {len(result['pages'])}

JavaScript Files : {len(result['javascript'])}

API Endpoints : {len(result['apis'])}
""",
            title="Crawler Summary",
        )
    )