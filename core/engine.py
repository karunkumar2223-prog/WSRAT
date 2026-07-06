from rich.console import Console
from rich.progress import Progress

console = Console()


class ScanEngine:

    def __init__(self):

        self.results = {}

    def run_module(self, name, function, *args):

        try:

            result = function(*args)

            self.results[name] = result

            return result

        except Exception as e:

            self.results[name] = str(e)

            return None

    def summary(self):

        console.print()

        console.rule("[bold green]Executed Modules[/bold green]")

        for module in self.results:

            console.print(f"✔ {module}")

        console.rule()