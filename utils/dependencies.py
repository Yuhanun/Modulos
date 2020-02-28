import os
import json

from typing import Iterable, Tuple

from utils.git_manager import get_local_repo_path, update_repo_local

def get_dependencies_folder(dir: str = ".") -> str:
    return os.path.abspath(f"{dir}/.modulos/dependencies")

def get_dependencies_file(dir: str = ".") -> str:
    return get_dependencies_folder(dir) + '/dependencies.json'

def get_dependencies_info(dir: str = ".") -> dict:
    return json.load(open(get_dependencies_file(dir)))

def get_dependency_info(name: str, version: str, dir: str = ".") -> dict:
    return get_dependencies_info(dir).get(name, {}).get(version)

def add_depdency(name: str, version: str, dir: str = ".") -> bool:
    """
    Adds a dependency to toml file,
    false if already exists
    true if not
    None if not found
    """
    
def get_path(name: str, version: str, dir: str = ".") -> str:
    """
    Gets path of a certain dependency

    :name: Name of dependency
    :version: Version of dependency
    :dir: directory to search in (root, so `{dir}/.modulos/dependencies` is where it searches)
    """
    return f"{dir}/.modulos/dependencies/{name}/{version}"

def is_installed(name: str, version: str, dir: str = ".") -> bool:
    """
    Checks if a certain dependency is already installed
    If it's installed -> true
    if not -> false

    :name: Name of dependency
    :version: Version of dependency
    :dir: directory to search in (root, so `{dir}/.modulos/dependencies` is where it searches)
    """
    return os.path.isdir(get_path(name, version, dir))

def get_dependencies(dir: str = ".") -> Iterable[Tuple[str, str]]:
    """
    Gets an iterable of tuples, (name, version) of dependencies for
    {dir}/modulos.toml
    """
    with open(get_dependencies_file(dir)) as file:
        data = json.load(file)

    output = []
    for name, value in data.items():
        output.extend([(name, v, ) for v in value])

    print(output)
    return output

def get_dependency_url(name: str, version: str, dir: str) -> str:
    """
    Gets the URL to a dependency
    """
    with open(get_local_repo_path(dir) + f"/{name}") as file:
        data = json.load(file)
    
    return data['url'] + "?commit=" + data['versions'][version]['hash']

def install_dependency(name: str, version: str, dir: str) -> bool:
    """
    Installs a dependency into {dir}/.modulos/dependencies/{name}/{version}
    """
    path = get_local_repo_path(dir)
    url = get_dependency_url(name, version, dir)
    print(url)
    # with open(f"{path}/{name}") as file:
        # data = json.load(file)
    
    # print(data)


def install_dependencies(dir: str = "."):
    """
    Installs all dependencies for current modulos package
    :dir: Current modulos package dir
    """
    print("Installing dependencies...")
    update_repo_local(dir)
    for name, version in get_dependencies(dir):
        install_dependency(name, version, dir)
