import os
import argparse

from utils.config_handler import load_config, is_module, save_config
from utils.color import error, success
from utils.dependencies import is_valid_version

def main(parser: argparse.Namespace) -> int:
    """
    Function that handles `modulos add`

    :parser: Argument parser used for command line input
    :return: integer status code, 0 == good
    """

    directory = parser.dir

    if not is_module(directory):
        error(f"Directory {os.path.abspath(directory)} is not a modulos module")
        return 1

    if parser.lib is None:
        error(f"`modulos lib` requires a --lib argument, such as --lib=nlohmann-json=1.0.0")
        return 1

    _, value = load_config(directory)

    split_data = parser.lib.split("=")
    if len(split_data) != 2:
        error(f"Invalid input for lib: {parser.lib}, format: --lib=name=version")
        return 1

    name, version = split_data

    version_data = is_valid_version(name, version, directory)
    if version_data is None:
        error(f"Module with name \"{name}\" does not exist")
        return 1

    if isinstance(version_data, list):
        error(f"Module with name\"{name} does not have version: {version}\"\n       Valid Versions: {' '.join(version_data)}")
        return 1

    value['dependencies'][name] = version
    value = save_config(value, directory)
    if not value:
        error("Could not save modulos.toml file.")
        return 1

    success(f"Added {name}, with version {version} to modulos.toml")
    return 0
