import json
import os

from jinja2 import Environment, FileSystemLoader
from urllib.parse import urlparse

from core.pdf_report import create_pdf_report


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
            score=score,
            results=results,
            total_modules=len(results),
        )

        html_path = f"reports/html/{filename}.html"

        with open(html_path, "w", encoding="utf-8") as file:
            file.write(html)

        print(f"\n✔ HTML Report : {html_path}")

        json_path = ReportGenerator.save_json(results, target)
        print(f"✔ JSON Report : {json_path}")

        try:
            pdf = create_pdf_report(target, results)
            print(f"\n✔ PDF Report : {pdf}")

        except Exception as e:
            import traceback
            traceback.print_exc()

        return html_path