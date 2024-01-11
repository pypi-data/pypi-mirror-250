#!/usr/bin/env python3

# Copyright 2021-2023 M. Farzalipour Tabriz, Max Planck Computing and Data Facility (MPCDF)
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the 3-Clause BSD License. See the LICENSE file for details.

""" 
By directly running this script, it tries to spawn a webserver on port 8080 serving files from "./" 
and redirecting non-existing {url} to {url}.html

  ./webserver.py

You can pass "SERVER_PORT" "SERVER_PATH" "REDIRECT" "VERBOSITY_LEVEL" variables as cli parameters.

You can also use this as a library and start it by calling ``start_webserver()`` python function
which takes care of reconfiguring and restarting the webserver in case it fails to start.
"""

import http.server
import os
import socket
import socketserver
import subprocess
import sys
import time

import requests

from linkmedic.logbook import init_logger


class MedicServer:
    """contains popen object for the server subprocess
    and information about the server configuration

    """

    online = False
    port = 0
    root_url = ""
    domain = ""
    redirect = False
    handle = None

    def __init__(self, port, root_url, redirect, domain):
        self.port = port
        self.root_url = root_url
        self.redirect = redirect
        self.domain = domain

    def __del__(self):
        if self.handle:
            self.handle.terminate()

    def relative_address(self, url: str):
        """returns address relative to the website root

        :param url:

        """
        return url.replace(self.root_url, "")


def start_webserver(
    requested_port: int = 8080,
    server_root_path: str = "./",
    domain: str = "",
    redirect: bool = True,
    verbosity_level: int = 3,
):
    """Start a webserver and return the address to its root

    :param requested_port: requested port (may or may not be available)
    :returns: an instance of MedicServer

    """
    newserver = MedicServer(requested_port, server_root_path, redirect, domain)
    server_connection_timeout = 0.5
    CONNECTION_TIMEOUT_MAX = 5
    logger = init_logger("webmaster", verbosity_level)

    exec_dir = os.path.dirname(os.path.abspath(__file__))

    # Try to start a webserver
    while not newserver.online:
        logger.debug("Checking port %d", newserver.port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
            test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if test_socket.connect_ex(("localhost", newserver.port)) == 0:
                logger.info("Port %d is not avaiable!", newserver.port)
                newserver.port += 1
                continue
            logger.debug("Port %d seems to be free!", newserver.port)

        newserver.root_url = "http://localhost:" + str(newserver.port)
        logger.info("Starting test webserver on port %d", newserver.port)
        newserver.handle = subprocess.Popen(
            [
                "python3",
                os.path.join(exec_dir, "webserver.py"),
                str(newserver.port),
                server_root_path,
                str(newserver.redirect),
                str(verbosity_level),
            ],
        )
        time.sleep(server_connection_timeout)

        try:
            server_exit = newserver.handle.poll()
            if server_exit:
                raise ChildProcessError(
                    "Webserver exited unexpectedly! Exit code: " + str(server_exit)
                )
            requests.get(newserver.root_url, timeout=server_connection_timeout)
            logger.info("Webserver started!")
            newserver.online = True
        except Exception as startup_err:
            logger.debug(startup_err)
            newserver.handle.terminate()
            newserver.port += 1
            if server_connection_timeout < CONNECTION_TIMEOUT_MAX:
                server_connection_timeout += 0.1
                logger.debug(
                    "Connection timeout adjusted to %0.1f s", server_connection_timeout
                )

    return newserver


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    """ """

    # pylint: disable-next=redefined-builtin
    def log_message(self, format, *args):
        """log webserver messages only at debug

        :param format:
        :param *args:

        """
        logger.debug(format, *args)

    def do_GET(self):
        """selectively redirect missing pages to .html"""
        if REDIRECT:
            if not os.path.exists(os.getcwd() + self.path) and os.path.exists(
                os.getcwd() + self.path + ".html"
            ):
                logger.debug("Redirecting: %s -> %s.html", self.path, self.path)
                self.path += ".html"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


if __name__ == "__main__":
    SERVER_PORT = int(sys.argv[1]) if sys.argv[1:] else 8080
    SERVER_PATH = sys.argv[2] if sys.argv[2:] else "./"
    REDIRECT = sys.argv[3] == "True" if sys.argv[3:] else False
    VERBOSITY_LEVEL = int(sys.argv[4]) if sys.argv[4:] else 3

    logger = init_logger("webserver", VERBOSITY_LEVEL)

    os.chdir(SERVER_PATH)
    logger.debug("Requested webserver port       : %s", SERVER_PORT)
    logger.debug("Requested webserver path       : %s", SERVER_PATH)
    logger.debug("Redirect missing pages to .html: %r", REDIRECT)

    try:
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", SERVER_PORT), MyHttpRequestHandler) as server:
            server.serve_forever()
    except Exception as server_err:
        logger.debug(server_err)
        sys.exit(1)
