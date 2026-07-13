import requests

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

TIMEOUT = 5

SENSITIVE_FILES = [
    ".env",
    ".git/config",
    ".git/HEAD",
    ".gitignore",
    ".htaccess",
    ".htpasswd",
    "config.php",
    "config.json",
    "config.yml",
    "config.yaml",
    "settings.py",
    "settings.json",
    "backup.zip",
    "backup.tar.gz",
    "backup.sql",
    "database.sql",
    "db.sql",
    "dump.sql",
    "phpinfo.php",
    "robots.txt",
    "sitemap.xml",
    "crossdomain.xml",
    "clientaccesspolicy.xml",
    ".DS_Store",
    "web.config",
    "server-status",
    "composer.json",
    "composer.lock",
    "package.json",
    "package-lock.json",
    "yarn.lock",
    ".svn/entries",
    ".hg/hgrc",
    ".bzr/",
    ".env.production",
    ".env.dev",
    ".env.local",
    ".aws/credentials",
    ".npmrc",
    "id_rsa",
    "id_dsa",
    "credentials.json",
    "secret.txt",
    "secrets.txt",
    "debug.log",
    "error.log",
    "access.log",
    "swagger.json",
    "openapi.json",
]

INTERESTING_CODES = [
    200,
    206,
    301,
    302,
    401,
    403,
]


def check_file(base_url, filename):

    url = base_url.rstrip("/") + "/" + filename

    try:

        r = requests.get(
            url,
            timeout=TIMEOUT,
            allow_redirects=False,
        )

        if r.status_code in INTERESTING_CODES:

            return {
                "file": filename,
                "status": r.status_code,
                "length": len(r.text),
            }

    except Exception:
        pass

    return None


def analyze_sensitive_files(url):

    findings = []

    for filename in SENSITIVE_FILES:

        result = check_file(url, filename)

        if result:
            findings.append(result)

    score = max(100 - len(findings) * 7, 0)

    return {
        "findings": findings,
        "score": score,
    }


def display_sensitive_files(result):

    table = Table(title="Sensitive Files Discovery")

    table.add_column("File")
    table.add_column("Status")
    table.add_column("Size")

    for item in result["findings"]:

        table.add_row(
            item["file"],
            str(item["status"]),
            str(item["length"]),
        )

    console.print(table)

    if result["score"] >= 90:
        risk = "Low"
    elif result["score"] >= 70:
        risk = "Medium"
    else:
        risk = "High"

    console.print(
        Panel.fit(
            f"""
Sensitive Files Score

{result['score']}/100

Files Found : {len(result['findings'])}

Risk Level : {risk}
""",
            title="Sensitive Files Summary",
        )
    )