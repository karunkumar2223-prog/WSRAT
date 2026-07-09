from concurrent.futures import ThreadPoolExecutor

from scanners.headers import (
    check_security_headers,
    display_headers,
)
from scanners.ssl import (
    analyze_ssl,
    display_ssl,
)
from scanners.cookies import (
    analyze_cookies,
    display_cookies,
)
from scanners.csp import (
    analyze_csp,
    display_csp,
)
from scanners.http_versions import (
    analyze_http_versions,
    display_http_versions,
)
from scanners.missing_headers import (
    analyze_missing_headers,
    display_missing_headers,
)
from scanners.technology import (
    analyze_technology,
    display_technology,
)
from scanners.subdomains import (
    analyze_subdomains,
    display_subdomains,
)
from scanners.directory import (
    analyze_directories,
    display_directories,
)

from scanners.dns import (
    analyze_dns,
    display_dns,
)


class ScanEngine:

    def __init__(self, url, response):
        self.url = url
        self.response = response

    def run(self):

        results = {}

        with ThreadPoolExecutor(max_workers=8) as executor:

            futures = {}

            futures["headers"] = executor.submit(
                check_security_headers,
                self.response,
            )

            futures["cookies"] = executor.submit(
                analyze_cookies,
                self.response,
            )

            futures["csp"] = executor.submit(
                analyze_csp,
                self.response,
            )

            futures["http"] = executor.submit(
                analyze_http_versions,
                self.url,
            )

            futures["missing_headers"] = executor.submit(
                analyze_missing_headers,
                self.response,
            )

            futures["technology"] = executor.submit(
                analyze_technology,
                self.response,
            )

            futures["subdomains"] = executor.submit(
                analyze_subdomains,
                self.url,
            )

            futures["directories"] = executor.submit(
                analyze_directories,
                self.url,
            )

            futures["dns"] = executor.submit(
                analyze_dns,
                self.url,
            )

            if self.url.startswith("https://"):
                futures["ssl"] = executor.submit(
                    analyze_ssl,
                    self.url,
                )

            for name, future in futures.items():
                results[name] = future.result()

        return results

    def display(self, results):

        display_headers(results["headers"])
        print()

        if "ssl" in results:
            display_ssl(results["ssl"])
            print()

        display_cookies(results["cookies"])
        print()

        display_csp(results["csp"])
        print()

        display_http_versions(results["http"])
        print()

        display_missing_headers(results["missing_headers"])
        print()

        display_subdomains(results["subdomains"])
        print()

        display_directories(results["directories"])
        print()

        display_technology(results["technology"])
        print()

        display_dns(results["dns"])
        print()