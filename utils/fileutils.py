import os

import glob
from typing import Iterable, Union


def get_include_dirs(path: str = ".") -> Iterable[str]:
    """
    Gets all folders in current directory

    :path: Current directory
    :returns: An iterable of absolute paths
    """
    return [os.path.abspath(each) for each in glob.glob(f"{path}/*", recursive=True) if os.path.isdir(each)]


def get_files_matching(extensions: Iterable[str], base_path: str = "", relative: bool = False):
    """Gets all files matching the extensions inputted relative to base_path

    :extensions: Extensions to get, as an iterable, for example ['cpp', 'c', 'cc']
    :base_path: Base path to search from, recursively
    :returns: Returns an iterable of absolute paths, for example ['/usr/test/test.cpp', '/sr/test/help.cc']
    """

    files = []
    for extension in extensions:
        files_matching = glob.glob(f"{base_path}**/*.{extension}", recursive=True)
        files.extend(
            map(os.path.abspath if not relative else lambda file: file,
                files_matching)
        )

    return files
