import logging
import warnings

import coloredlogs


# pylint: disable-next=unused-argument
def basic_warning_format(message, category, filename, lineno, *args, **kwargs):
    return "%s: %s" % (category.__name__, message)


# pylint: disable-next=unused-argument
def detailed_warning_format(message, category, filename, lineno, *args, **kwargs):
    return "%s:%s: %s: %s" % (filename, lineno, category.__name__, message)


def init_logger(logger_name, verbosity_level):
    """initialize the logger with a given name and verbosity

    :param logger_name:
    :param verbosity_level: 0,1,2,3(+)

    """
    logging.captureWarnings(True)
    warnings.formatwarning = basic_warning_format

    logger_handle = logging.getLogger(logger_name)
    logging_format = "%(levelname)-7s %(message)s"
    if verbosity_level == 0:
        logging.disable(logging.CRITICAL)
    else:
        if verbosity_level == 1:
            coloredlogs_level = "error"
            logging_level = logging.ERROR
        elif verbosity_level == 2:
            coloredlogs_level = "info"
            logging_format = "%(levelname)-7s %(name)-11s %(message)s"
            logging_level = logging.INFO
        else:
            coloredlogs_level = "debug"
            logging_format = "%(levelname)-7s %(name)-22s %(message)s"
            logging_level = logging.DEBUG
            warnings.formatwarning = detailed_warning_format

        logging.getLogger("urllib3").setLevel(logging_level)
        logger_handle.debug(
            'Initialized logger "%s" with level "%s"', logger_name, logging_level
        )
        coloredlogs.install(level=coloredlogs_level, fmt=logging_format)
        logger_handle.debug('Installing coloredlogs with level "%s"', coloredlogs_level)
    return logger_handle
