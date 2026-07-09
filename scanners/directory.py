import concurrent.futures
from pathlib import Path

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

TIMEOUT = 5
MAX_THREADS = 20


def check_path(base_url, path):
    url = base_url.rstrip("/") + "/" + path.lstrip("/")

    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            allow_redirects=False,
        )

        return {
            "path": "/" + path,
            "status": response.status_code,
        }

    except requests.RequestException:
        return None


def load_wordlist():
    """
    Load directory wordlist.
    Prefer directories.txt.
    Fallback to common.txt.
    """

    base = Path(__file__).resolve().parent.parent / "wordlists"

    directory_list = base / "directories.txt"
    common_list = base / "common.txt"

    if directory_list.exists():
        file = directory_list
    elif common_list.exists():
        file = common_list
    else:
        raise FileNotFoundError(
            "No wordlist found. Expected directories.txt or common.txt."
        )

    with open(file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def calculate_score(findings):
    """
    Simple directory exposure score.
    More exposed resources = lower score.
    """

    score = 100

    for item in findings:
        status = item["status"]

        if status == 200:
            score -= 8
        elif status in [301, 302]:
            score -= 5
        elif status == 401:
            score -= 3
        elif status == 403:
            score -= 2

    return max(score, 0)


def risk_level(score):

    if score >= 85:
        return "Low"

    if score >= 60:
        return "Medium"

    return "High"


def analyze_directories(url):

    words = load_wordlist()

    findings = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_THREADS
    ) as executor:

        futures = [
            executor.submit(check_path, url, word)
            for word in words
        ]

        for future in concurrent.futures.as_completed(futures):

            result = future.result()

            if result and result["status"] in (
                200,
                301,
                302,
                401,
                403,
            ):
                findings.append(result)

    findings.sort(key=lambda x: x["path"])

    score = calculate_score(findings)

    return {
        "findings": findings,
        "score": score,
        "risk": risk_level(score),
    }


def display_directories(result):

    table = Table(title="Directory Enumeration")

    table.add_column("Path", style="cyan")
    table.add_column("Status", justify="center")

    for item in result["findings"]:

        status = item["status"]

        if status == 200:
            status_text = "[green]200 OK[/green]"

        elif status in [301, 302]:
            status_text = "[blue]Redirect[/blue]"

        elif status == 401:
            status_text = "[yellow]401 Unauthorized[/yellow]"

        elif status == 403:
            status_text = "[orange3]403 Forbidden[/orange3]"

        else:
            status_text = str(status)

        table.add_row(
            item["path"],
            status_text,
        )

    console.print(table)

    console.print(
        Panel.fit(
            f"""
[bold green]Directory Security Assessment[/bold green]

Directory Score : {result['score']}/100

Resources Found : {len(result['findings'])}

Risk Level : {result['risk']}
""",
            title="Directory Summary",
        )
    )