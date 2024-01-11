# Copyright 2021-2023 M. Farzalipour Tabriz, Max Planck Computing and Data Facility (MPCDF)
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the 3-Clause BSD License. See the LICENSE file for details.


import json
import logging
import os
import re
from http import HTTPStatus
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, SoupStrainer

from linkmedic.logbook import init_logger
from linkmedic.reception import Orders
from linkmedic.webserver import MedicServer


class LinksStatus:
    """Aggregated statistics on status of tested links."""

    tested_links = 0
    dead_links = 0
    ignored_dead_links = 0
    http_links = 0
    parsed_urls = set()

    def __add__(self, other):
        total = self
        total.tested_links += other.tested_links
        total.dead_links += other.dead_links
        total.ignored_dead_links += other.ignored_dead_links
        total.http_links += other.http_links
        total.parsed_urls.update(other.parsed_urls)
        return total

    def __str__(self):
        parsed_links = len(self.parsed_urls)
        alive_links = self.tested_links - self.dead_links - self.ignored_dead_links

        stat_line = (
            "Discovered unique links: "
            + str(parsed_links)
            + " | "
            + str(self.tested_links)
            + " Tested | "
            + str(alive_links)
            + " Alive | "
            + str(self.dead_links)
            + " Dead ("
            + str(self.ignored_dead_links)
            + " ignored) || "
            + str(self.http_links)
            + " HTTP WARNING"
        )

        return stat_line

    def write_badge_files(self, tests_done: Orders):
        """write json badge description files

        :param tests_done: test orders performed

        """
        if not tests_done.internal_check:
            badge_name = "dead_external_links"
        elif not tests_done.external_check:
            badge_name = "dead_internal_links"
        else:
            badge_name = "dead_links"

        write_json_badge(badge_name, self.dead_links)

        if tests_done.http_check:
            http_badge_name = "http_links"
            write_json_badge(http_badge_name, self.http_links, critical=False)


def fetch_url(url: str):
    """

    :param url:
    :returns: http request response

    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    return requests.get(url, headers=headers, timeout=5)


def check_life(server: MedicServer, url: str, order: Orders):
    """check status of a url

    :param url:
    :returns: alive, msg, ignored_status

    """
    logger = logging.getLogger("diagnose")
    ignored_status = False
    dead_links_http_status_default = set([400, 404, 403, 408, 409, 501, 502, 503])
    logger.debug("Checking: %s", url)

    if order.ignore_status is not None:
        dead_links_http_status = dead_links_http_status_default.difference(
            order.ignore_status
        )
    else:
        dead_links_http_status = dead_links_http_status_default

    try:
        response = fetch_url(url)
        if response.status_code in dead_links_http_status:
            msg = (
                "DEAD LINK ("
                + str(response.status_code)
                + "-"
                + HTTPStatus(response.status_code).phrase
                + ") -> "
                + server.relative_address(url)
            )
            alive = False
        else:
            if response.status_code in order.ignore_status:
                msg = (
                    "Got response "
                    + str(response.status_code)
                    + " from the server which will be ignored! -> "
                    + server.relative_address(url)
                )
                ignored_status = True
            else:
                msg = "OK! -> " + server.relative_address(url)
            alive = True
        return alive, msg, ignored_status
    except requests.exceptions.RequestException as requests_err:
        logger.debug(requests_err)
        msg = "CONNECTION FAILED -> " + server.relative_address(url)
        return False, msg, False


def link_cleanup(link: str, server: MedicServer, base_address: str) -> str:
    """

    :param link:
    :param base_address: the page in which this link has been encountered e.g. https://abc.de/here

    """
    if re.match("^#", link):  # anchor in the base_address
        return ""
    if re.match("^(mailto|tel):", link):
        return ""
    if re.match(r".*(#)\S+", link):  # page + anchor
        link = re.search(r"(.*)#\S+", link).group(1)
    if not re.match(r"^https?:\/{2}", link):  # relative to the base_address
        link = urljoin(base_address, link)

    if server.domain:
        if re.match(r"^https?:\/{2}" + server.domain + "(.*)", link):
            internal_path = re.search(
                r"^https?:\/{2}" + server.domain + "(.*)", link
            ).group(1)
            link = urljoin(server.root_url, internal_path)

    return link


def crawl_url(url: str, server: MedicServer, order: Orders):
    """parses the url and checks all it links.

    returns LinksStatus, discovered_pages

    :param url:

    """
    logger = logging.getLogger("diagnose")
    stats = LinksStatus()
    discovered_pages = set()
    html_link_tags = {
        "a": "href",
        "iframe": "src",
        "img": "src",
        "link": "href",
        "script": "src",
    }
    xml_link_tags = {
        "a": "xlink:href",
        "event-listener": "xlink:href",
    }
    no_follow_exts = (
        ".conf",
        ".gif",
        ".ico",
        ".jpeg",
        ".jpg",
        ".js",
        ".pdf",
        ".png",
        ".svg",
        ".tar.gz",
        ".txt",
        ".woff2",
        ".zip",
    )

    try:
        response = fetch_url(url)
        base_address = response.url  # handle redirects
        if base_address.endswith(".xml") or re.match(r".*\.fod[tsp]{1}$", base_address):
            content_parser = "xml"
            link_tags = xml_link_tags
        else:
            content_parser = "html.parser"
            link_tags = html_link_tags

        for link_tag, link_url in iter(link_tags.items()):
            for link_obj in BeautifulSoup(
                response.text, content_parser, parse_only=SoupStrainer(link_tag)
            ):
                if link_obj.has_attr(link_url):
                    new_url = link_cleanup(link_obj[link_url], server, base_address)
                    if new_url:
                        logger.debug(
                            "Parser returned a link: %s",
                            server.relative_address(new_url),
                        )
                        if new_url not in stats.parsed_urls:
                            stats.parsed_urls.add(new_url)
                            logger.debug(
                                "New link to check: %s",
                                server.relative_address(new_url),
                            )
                            alive = None
                            ignored = False
                            ignored_status = False
                            msg = ""
                            if (
                                server.relative_address(new_url)
                                not in order.ignore_urls
                            ):
                                if server.root_url in new_url:  # local links
                                    alive, msg, ignored_status = check_life(
                                        server, new_url, order
                                    )
                                    stats.tested_links += 1
                                    if (
                                        not alive
                                        and order.internal_check
                                        and not ignored_status
                                    ):
                                        stats.dead_links += 1
                                    if not alive and not order.internal_check:
                                        stats.ignored_dead_links += 1
                                        ignored = True
                                        msg = (
                                            "IGNORED DEAD INTERNAL LINK -> "
                                            + server.relative_address(new_url)
                                        )

                                    if not new_url.endswith(no_follow_exts):
                                        logger.debug(
                                            "Links in this page should be followed -> %s",
                                            server.relative_address(new_url),
                                        )
                                        discovered_pages.add(new_url)

                                    else:
                                        logger.debug(
                                            "Links in this page will be ignored -> %s",
                                            server.relative_address(new_url),
                                        )
                                else:  # external links
                                    if order.external_check:
                                        alive, msg, ignored_status = check_life(
                                            server, new_url, order
                                        )
                                        stats.tested_links += 1
                                        if not alive and not ignored_status:
                                            stats.dead_links += 1
                                        if order.http_check:
                                            if "http://" in new_url:
                                                http_msg = "HTTP LINK -> " + new_url
                                                log_status(
                                                    http_msg,
                                                    "yellow",
                                                    server.relative_address(
                                                        base_address
                                                    ),
                                                )
                                                stats.http_links += 1
                                    else:
                                        ignored = True
                                        alive = True
                                        msg = "IGNORED EXTERNAL LINK -> " + new_url

                            else:  # url in ignore list
                                ignored = True
                                alive = True
                                msg = (
                                    "PAGE IN IGNORE LIST -> "
                                    + server.relative_address(new_url)
                                )
                            if not alive and ignored_status:
                                stats.ignored_dead_links += 1
                                msg_color = "yellow"
                            if ignored:
                                msg_color = "green" if alive else "yellow"
                            else:
                                msg_color = "green" if alive else "red"
                            log_status(
                                msg, msg_color, server.relative_address(base_address)
                            )
                        else:
                            logger.debug(
                                "Link was discovered before: %s",
                                server.relative_address(new_url),
                            )
        return stats, discovered_pages
    except Exception as crawler_err:
        logger.error("%s : %s", url, crawler_err)
        stats.dead_links += 1
        return stats, discovered_pages


def log_status(msg: str, color: str, page_url: str):
    """

    :param msg: param color:
    :param page_url: url for the page which cointains the link
    :param color:

    """
    logger = logging.getLogger("diagnose")
    if not msg:
        logger.warning("Internal error! log_status() was called with an empty message.")
        return

    if color == "green":
        msg_level = 10
    elif color == "yellow":
        msg_level = 30
    else:
        msg_level = 40

    msg = "@" + page_url + " > " + msg

    logger.log(msg_level, msg)


def write_json_badge(name: str, val: int, critical: bool = True):
    """

    :param name:
    :param val:
    :param critical: Default value = True

    """
    logger = logging.getLogger("diagnose")
    file = "badge." + name + ".json"
    badge_label = name.replace("_", "%20")

    if os.path.isfile(file):
        logger.debug("Overwriting the old badge info file: %s", file)
    else:
        logger.debug("Writing badge info file: %s", file)

    if val == 0:
        badge_color = "green"
    else:
        if critical:
            badge_color = "red"
        else:
            badge_color = "yellow"

    badge_data = {
        "schemaVersion": 1,
        "label": badge_label,
        "message": val,
        "color": badge_color,
    }
    with open(file, "w", encoding="utf-8") as json_file:
        json.dump(badge_data, json_file, ensure_ascii=False, indent=4)


def diagnose(server: MedicServer, entry: str, order: Orders, verbosity_level) -> int:
    ENTRY_URL = server.root_url + "/" + entry
    uncrawled_urls = set()
    stats = LinksStatus()
    logger = init_logger("diagnose", verbosity_level)
    logger.debug("Adding entry page's URL to the list: %s", ENTRY_URL)
    uncrawled_urls.add(ENTRY_URL)

    logger.info("Starting the crawler")
    try:
        # the entry page is checked separately!
        stats.parsed_urls.add(ENTRY_URL)
        alive, msg, _ = check_life(server, ENTRY_URL, order)
        stats.tested_links += 1
        msg_color = "green" if alive else "red"
        log_status(msg, msg_color, "$")
        if not alive:
            stats.dead_links = 1
            raise FileNotFoundError(
                "The entry page could not be loaded: "
                + server.relative_address(ENTRY_URL)
            )

        while uncrawled_urls:
            new_url = uncrawled_urls.pop()
            new_stats, extracted_urls_list = crawl_url(new_url, server, order)
            stats += new_stats
            if extracted_urls_list:
                logger.debug("Crawler extracted urls: %s", str(extracted_urls_list))
                uncrawled_urls.update(extracted_urls_list)

        logger.info("Crawler finished checking pages")

        if order.write_badge:
            logger.info("Writing badge files")
            stats.write_badge_files(order)
        logger.info(stats)
        RETURN_CODE = int(stats.dead_links > 0)
    except Exception as err:
        logger.error(err)
        RETURN_CODE = 2

    return RETURN_CODE
