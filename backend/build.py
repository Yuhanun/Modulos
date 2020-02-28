import os

import argparse
from typing import Iterable
import distutils.spawn

from utils import fileutils, config_handler, color


def generate_command(base_path: str, source_files: Iterable[str], header_directories: Iterable[str], dependencies: Iterable[str]):
    command = ""

    compiler = config_handler.get_compiler(base_path)
    if not compiler:
        return False, f"Path \"{compiler}\" is not a valid compiler"

    compiler = distutils.spawn.find_executable(compiler)

    if not compiler:
        return False, f"Path \"{compiler}\" is not a valid compiler"

    command += f"{compiler}"

    for cpp_file in source_files:
        command += f" {cpp_file}"

    command += f" -o {config_handler.get_output_path(base_path)}"

    return True, command


def main(parser: argparse.Namespace) -> int:
    """
    Function that handles `modulos.build`

    :parser: Argument parser used for command line input
    :return: integer status code, 0 == good
    """
    base_path = (parser.dir + "/") or "."

    if not config_handler.is_module(base_path):
        color.error(f"Directory {base_path} is not a modulos module")
        return 1

    dependencies = []
    source_files = fileutils.get_files_matching(
        ["cpp", "cc", "cxx"], base_path=base_path)
    include_dirs = fileutils.get_include_dirs(f"{base_path}/include")

    status, data = generate_command(
        base_path, source_files, include_dirs, dependencies)

    if not status:
        color.error(data)
        return 1

    compile_status = os.system(data)

    color.write(
        f"Compiler exited with status: {compile_status}", not compile_status)
    return 0
