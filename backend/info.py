import pprint

import argparse

from utils.color import error, success
from utils.dependencies import get_dependency_info


def main(parser: argparse.Namespace) -> int:
    """
    Function that handles `modulos info`

    :parser: Argument parser used for command line input
    :return: integer status code, 0 == good
    """
    if not parser.dep:
        error(f"No dependency was given for modulos info")
        return 1

    name, version = parser.dep.split("=")

    info = get_dependency_info(name, version, parser.dir)

    if not info:
        error(f"No dependency called {name} with version {version} was found")
        return 1

    success(f"\n{name = }\n{version = }")
    pprint.pprint(info)

    return 0
