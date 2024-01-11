import argparse
import os
import re

from linkmedic.__init__ import __version__


class Orders:
    """Diagnostic orders for the link medic"""

    internal_check = False
    external_check = False
    http_check = False
    write_badge = False
    ignore_status = set()
    ignore_urls = set()

    def __init__(self, args_namespace):
        self.internal_check = not args_namespace.ignore_local
        self.external_check = args_namespace.check_external
        self.http_check = args_namespace.warn_http
        self.write_badge = args_namespace.with_badge
        self.ignore_status = set(args_namespace.ignore_status)

        if not (self.internal_check or self.external_check):
            self.external_check = True

        LINKS_IGNORE_FILE_PATH = os.path.join(args_namespace.root, ".linkignore")
        LINKS_IGNORE_FILE_FOUND = os.path.isfile(LINKS_IGNORE_FILE_PATH)
        if LINKS_IGNORE_FILE_FOUND:
            with open(
                LINKS_IGNORE_FILE_PATH, "r", encoding="utf-8"
            ) as linksignore_file:
                for ignore_item in linksignore_file.read().splitlines():
                    sanitized_ignore_item = ignore_item.strip().lower()
                    if sanitized_ignore_item[0] != "/" and not re.match(
                        r"^https?:\/{2}.*", sanitized_ignore_item
                    ):
                        sanitized_ignore_item = "/" + sanitized_ignore_item
                    self.ignore_urls.add(sanitized_ignore_item)


def cli_args():
    """returns cli arguments"""
    parser = argparse.ArgumentParser(description="Simple python website links checker")
    parser.add_argument(
        "-r",
        "--root",
        default="./",
        help="path of the webserver's root folder (default=./)",
    )
    parser.add_argument(
        "-e",
        "--entry",
        default="index.html",
        help="path of the entry page on the webserver, relative to the root (default=index.html)",
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parser.add_argument("--quiet", action="store_true", help="show only error logs")
    parser.add_argument("--silent", action="store_true", help="slience the output logs")
    parser.add_argument("--exit-zero", action="store_true", help="always return zero")
    parser.add_argument(
        "--no-redirect",
        action="store_true",
        help="do not redirect the 'missing_page' to 'missing_page.html'",
    )
    parser.add_argument(
        "--check-external", action="store_true", help="check links to external domains"
    )
    parser.add_argument(
        "--ignore-local", action="store_true", help="ignore local dead links"
    )
    parser.add_argument(
        "--ignore-status",
        type=int,
        nargs="*",
        help="ignore these HTTP status codes",
        metavar="HTTP status code",
        default=[],
    )
    parser.add_argument(
        "--warn-http", action="store_true", help="show warning for http links"
    )
    parser.add_argument(
        "--with-badge",
        action="store_true",
        help="generate a badge info file in json format"
        "(can be passed to linkmedkit scripts or shields.io API)",
    )
    parser.add_argument(
        "--port", type=int, help="webserver's port (default=8080)", default=8080
    )
    parser.add_argument(
        "--domain",
        help="name of the webserver's domain which its links will be treated as internal",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__
    )
    return parser.parse_args()
