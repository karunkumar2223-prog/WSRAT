import socket
from urllib.parse import urlparse

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP Alt",
    8443: "HTTPS Alt",
}


def scan_port(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((host, port))

    sock.close()

    return result == 0


def analyze_ports(url):

    hostname = urlparse(url).hostname

    open_ports = []

    for port, service in COMMON_PORTS.items():

        try:

            if scan_port(hostname, port):

                open_ports.append({
                    "port": port,
                    "service": service
                })

        except Exception:
            pass

    score = max(100 - (len(open_ports) * 5), 0)

    if len(open_ports) <= 2:
        risk = "Low"
    elif len(open_ports) <= 5:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "open_ports": open_ports,
        "score": score,
        "risk": risk
    }


def display_ports(result):

    table = Table(title="Port Scanner")

    table.add_column("Port")
    table.add_column("Service")
    table.add_column("Status")

    if result["open_ports"]:

        for port in result["open_ports"]:

            table.add_row(
                str(port["port"]),
                port["service"],
                "Open"
            )

    else:

        table.add_row("-", "-", "No Open Ports Found")

    console.print(table)

    console.print(
        Panel.fit(
            f"""
Port Security Score

{result['score']}/100

Open Ports : {len(result['open_ports'])}

Risk Level : {result['risk']}
""",
            title="Port Summary"
        )
    )