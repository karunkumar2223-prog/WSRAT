from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def analyze_cookies(response):
    """
    Analyze cookies received from the HTTP response.
    """

    cookies = []

    for cookie in response.cookies:

        rest = getattr(cookie, "_rest", {})

        cookies.append({
            "name": cookie.name,
            "secure": cookie.secure,
            "httponly": "HttpOnly" in rest,
            "samesite": rest.get("SameSite", "Missing"),
            "domain": cookie.domain,
            "path": cookie.path,
            "expires": cookie.expires
        })

    return cookies


def calculate_cookie_score(cookies):

    if len(cookies) == 0:
        return 100

    score = 100

    for cookie in cookies:

        if not cookie["secure"]:
            score -= 15

        if not cookie["httponly"]:
            score -= 15

        if cookie["samesite"] == "Missing":
            score -= 10

    return max(score, 0)


def display_cookies(cookies):

    table = Table(title="Cookie Security Analysis")

    table.add_column("Cookie", style="cyan")
    table.add_column("Secure")
    table.add_column("HttpOnly")
    table.add_column("SameSite")
    table.add_column("Domain")
    table.add_column("Path")

    for cookie in cookies:

        table.add_row(
            cookie["name"],
            "Yes" if cookie["secure"] else "No",
            "Yes" if cookie["httponly"] else "No",
            str(cookie["samesite"]),
            cookie["domain"],
            cookie["path"]
        )

    console.print(table)

    score = calculate_cookie_score(cookies)

    console.print(
        Panel.fit(
            f"""
[bold green]Cookie Security Score[/bold green]

{score}/100

Total Cookies : {len(cookies)}
""",
            title="Cookie Summary",
            border_style="green"
        )
    )