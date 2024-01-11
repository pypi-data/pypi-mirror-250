import os
import re
import sys
import tempfile
import zipfile

from linkmedic.__init__ import __version__
from linkmedic.diagnose import diagnose
from linkmedic.logbook import init_logger
from linkmedic.reception import Orders, cli_args
from linkmedic.webserver import start_webserver


def main():
    ARGS = cli_args()
    do = Orders(ARGS)

    verbosity_level = 2 + ARGS.verbose
    if ARGS.quiet:
        verbosity_level = 1
    if ARGS.silent:
        verbosity_level = 0

    logger = init_logger("root", verbosity_level)

    logger.debug("linkmedic version %s", __version__)
    logger.debug("============================================================")
    logger.debug("webserver's root folder    : %s", ARGS.root)
    logger.debug("webserver port             : %d", ARGS.port)
    logger.debug("webserver's domain name    : %s", ARGS.domain)
    logger.debug("entry page                 : %s", ARGS.entry)
    logger.debug("entry page (expanded)      : %s", os.path.expanduser(ARGS.entry))
    logger.debug("redirect missing pages     : %r", not ARGS.no_redirect)
    logger.debug("check external links       : %s", ARGS.check_external)
    logger.debug("ignore local missing pages : %s", ARGS.ignore_local)
    logger.debug("ignore HTTP status codes   : %s", ARGS.ignore_status)
    logger.debug("warn http links            : %s", ARGS.warn_http)
    logger.debug("write badge info file      : %s", ARGS.with_badge)
    logger.debug("quiet output               : %r", ARGS.quiet)
    logger.debug("silence the output         : %r", ARGS.silent)
    logger.debug("verbosity level            : %s", verbosity_level)
    logger.debug("exit zero                  : %r", ARGS.exit_zero)
    logger.debug("Ignoring the links to      : %s", do.ignore_urls)
    logger.debug("============================================================")

    if not os.path.isdir(ARGS.root):
        logger.error("The webserver root path not found: %s", ARGS.root)
        sys.exit(2)

    if re.match(r".*\.[f]?od[tsp]{1}$", ARGS.entry):
        logger.debug("Entry page is an Open Document file")
        if not do.external_check:
            logger.debug(
                "Activating external links checking for the Open Document file"
            )
            do.external_check = True

        if re.match(r".*\.od[tsp]{1}$", ARGS.entry):
            tmp_dir = tempfile.TemporaryDirectory()
            logger.debug(
                "Created tmp directory for extracting Open Document file: %s",
                tmp_dir.name,
            )
            try:
                with zipfile.ZipFile(
                    os.path.expanduser(os.path.join(ARGS.root, ARGS.entry)), "r"
                ) as odf_archive:
                    odf_archive.extract("content.xml", path=tmp_dir.name)
            except Exception as err:
                logger.error(str(err))
                sys.exit(2)

            ARGS.root = tmp_dir.name
            ARGS.entry = "content.xml"

    server = start_webserver(
        ARGS.port,
        ARGS.root,
        ARGS.domain,
        not ARGS.no_redirect,
        verbosity_level,
    )
    logger.debug("Test webserver URL: %s", server.root_url)

    EXIT_CODE = diagnose(server, ARGS.entry, do, verbosity_level)

    if not ARGS.exit_zero:
        sys.exit(EXIT_CODE)


if __name__ == "__main__":
    main()
