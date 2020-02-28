import os

import argparse
import colorama

import utils.config_handler
from utils.color import write, error


def main(parser: argparse.Namespace) -> int:
    """
    Function that handles `modulos.init`

    :parser: Argument parser used for command line input
    :return: integer status code, 0 == good
    """
    if not parser.compiler:
        error("--compiler={compiler} has not been set in `init` call")
        return 1

    if not parser.version:
        error("--version={version} has not been set in `init` call")
        return 1

    status, response = utils.config_handler.init_config(
        parser.dir,
        parser.name or os.path.basename(os.getcwd()),
        parser.compiler,
        parser.version,
    )

    write(response, status)
    return not status
