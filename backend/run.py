import os

import argparse
import colorama

import utils.config_handler
from utils.color import write, error

from backend import build


def main(parser: argparse.Namespace) -> int:
    """
    Function that handles `modulos run`

    :parser: Argument parser used for command line input
    :return: integer status code, 0 == good
    """

    if build.main(parser):
        return 1

    output_path = utils.config_handler.get_output_path(
        parser.dir + "/", create=False)

    run_status = os.system(output_path)

    write(
        f"Binary \"{output_path}\" exited with status: {run_status}", not run_status)

    return not run_status
