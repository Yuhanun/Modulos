import os

import argparse
import shutil

from utils.color import error, success
from utils.config_handler import get_output_path, is_module, get_name
from utils.fileutils import get_all_folders


def main(parser: argparse.Namespace) -> int:
    """
    Function that handles `modulos clean`

    :parser: Argument parser used for command line input
    :return: integer status code, 0 == good
    """
    valid_module = is_module(parser.dir)
    if not valid_module:
        error(f"Directory {parser.dir} is not a modulos module")
        return 1

    path = get_output_path(parser.dir, create=False, add_binary=False)
    
    if path and os.path.isdir(path):
        shutil.rmtree(path)

    dependency_dirs = get_all_folders(parser.dir + ".modulos/dependencies")
    for path in dependency_dirs:
        shutil.rmtree(path)

    success(f"Cleaned package: {get_name(parser.dir)}")
    return 0
