import json
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from urllib.parse import urlparse


class ReportGenerator:

    @staticmethod
    def save_json(results, target):

        os.makedirs("reports/json", exist_ok=True)

        parsed = urlparse(target)
        filename = parsed.netloc.replace(":", "_")

        filepath = f"reports/json/{filename}.json"

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4, default=str)

        return filepath

    @staticmethod
    def save_html(results, target, score):

        os.makedirs("reports/html", exist_ok=True)

        parsed = urlparse(target)
        filename = parsed.netloc.replace(":", "_")

        env = Environment(
            loader=FileSystemLoader("templates")
        )

        template = env.get_template("report.html")

        html = template.render(
            target=target,
            generated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            score=score,
            results=results
        )

        filepath = f"reports/html/{filename}.html"

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(html)

        return filepath