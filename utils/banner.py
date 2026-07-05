from rich.console import Console
from rich.panel import Panel

console = Console()

def print_banner():
    console.print(
        Panel.fit(
            "[bold cyan]Web Security Recon & Assessment Toolkit[/bold cyan]\n"
            "[green]Version 1.0[/green]",
            title="WSRAT",
            border_style="cyan",
        )
    )