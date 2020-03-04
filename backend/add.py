import os
import argparse

from utils.config_handler import load_config, is_module
from utils.color import error, success
from utils.dependencies import is_valid_version

def main(parser: argparse.Namespace) -> int:
    """
    Function that handles `modulos add`

    :parser: Argument parser used for command line input
    :return: integer status code, 0 == good
    """

    if not is_module(dir):
        error(f"Directory {os.path.abspath(dir)} is not a modulos module")
        return 1

    _, value = load_config(parser.dir)

    split_data = parser.lib.split("=")
    if len(split_data) != 2:
        error(f"Invalid input for lib: {parser.lib}, format: --lib=name=version")
        return 1

    name, version = split_data

    version_data = is_valid_version(name, version, dir)
    if version_data is False:
        error(f"Module with name \"{name}\" does not exist")
        return 1

    if isinstance(version_data, dict):
        error(f"Module with name\"{name} does not have version: {version}\"\n     Valid Versions: {' '.join(version_data)}")
        return 1

    return 0
