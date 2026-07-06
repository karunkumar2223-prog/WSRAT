from rich.console import Console

console = Console()


class ScanEngine:
    def __init__(self, url):
        self.url = url
        self.results = {}

    def add_result(self, module, result):
        self.results[module] = result

    def get_results(self):
        return self.results

    def summary(self):
        console.print("\n[bold green]Modules Executed:[/bold green]")

        for module in self.results:
            console.print(f"[green]✔[/green] {module}")