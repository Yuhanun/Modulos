import os

import argparse
from typing import Iterable

from utils import fileutils, config_handler, color
from utils.dependencies import install_dependencies, get_dependency_binaries_includes, build_project


def main(parser: argparse.Namespace) -> int:
    """
    Function that handles `modulos.build`

    :parser: Argument parser used for command line input
    :return: integer status code, 0 == good
    """
    return build_project(parser)