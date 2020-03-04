import os
import json

from typing import Iterable, Tuple

from .git_manager import get_local_repo_path, update_repo_local, clone_dependency
from .color import error
from .config_handler import load_config, is_module

from backend import build

def get_dependencies_folder(dir: str = ".") -> str:
    return os.path.abspath(f"{dir}/.modulos/dependencies")


def get_dependencies_file(dir: str = ".") -> str:
    return get_dependencies_folder(dir) + '/dependencies.json'


def get_dependencies_info(dir: str = ".") -> dict:
    return json.load(open(get_dependencies_file(dir)))


def get_dependency_info(name: str, version: str, dir: str = ".") -> dict or None:
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
    return os.path.isdir(get_path(name, version, dir) + "/" + name)


def get_dependencies(dir: str = ".") -> Iterable[Tuple[str, str]]:
    """
    Gets an iterable of tuples, (name, version) of dependencies for
    {dir}/modulos.toml
    """
    # data = get_dependencies(dir)

    valid, config = load_config(dir)
    return tuple(config['dependencies'].items())


def load_dependency_json(name: str, dir: str) -> dict:
    """
    Loads a dependency config
    """
    with open(get_local_repo_path(dir) + f"/{name}") as file:
        return json.load(file)


def get_dependency_url(cfg: dict, version: str, dir: str) -> (str, str):
    """
    Gets the URL to a dependency
    (url, hash)
    """
    return cfg['url'], cfg['versions'][version]['hash']


def build_dependency(dir: str, name: str, version: str) -> bool:
    # build, modulos build probs but idk how
    
    dep_dir = get_path(name, version, dir)
    if not is_module(dep_dir):
        return False

    class Args:
        pass

    obj = Args()
    obj.dir = dep_dir
    current_dir = os.getcwd()
    os.chdir(dep_dir)
    build.main(obj)
    os.chdir(current_dir)

def set_dependency_info(dir: str, name: str, version: str, dep_json: dict):
    file_path = get_dependencies_file(dir)

    with open(file_path, 'r') as file:
        data = json.load(file)

    # TODO
    if name not in data:
        data[name] = {}
    data[name][version] = dep_json['versions'][version]
    del data[name][version]['hash']

    with open(file_path, 'w') as file:
        json.dump(data, file)
 
def install_dependency(name: str, version: str, dir: str) -> bool:
    """
    Installs a dependency into {dir}/.modulos/dependencies/{name}/{version}

    False if already installed
    True if not
    """
    print(f"Installing dependency: {name} = {version}")
    dep_json = load_dependency_json(name, dir)
    if is_installed(name, version, dir):
        set_dependency_info(dir, name, version, dep_json)
        return False

    path = get_path(name, version, dir)
    if os.path.isdir(path):
        os.rmdir(path)
    os.makedirs(path)
    url, hash = get_dependency_url(dep_json, version, dir)
    clone_dependency(dir, name, version, url, hash)
    build_dependency(dir, name, version)

    if not is_installed:
        error(f"Failed to install {name}:{version} in {os.path.abspath(dir)}")

    set_dependency_info(dir, name, version, dep_json)
    return True


def install_dependencies(dir: str = "."):
    """
    Installs all dependencies for current modulos package
    :dir: Current modulos package dir
    """
    print("Installing dependencies...")
    update_repo_local(dir)
    for name, version in get_dependencies(dir):
        install_dependency(name, version, dir)

def get_dependency_binaries_includes(dir: str = ".") -> dict:
    """
    Gets all include dirs from dependencies
    """
    data = get_dependencies_info(dir)
    info = {
        'include_dirs': [],
        'static_libraries': [],
        'dynamic_libraries': [],
    }

    for name, versions in data.items():
        for version_str, version_info in versions.items():
            base_path = get_path(name, version_str, dir) + f"/{name}/"
            for key in version_info:
                [info[key].append(base_path + dep_file) for dep_file in version_info[key]]
    
    return info

# install_dependency("nlohmann-json", "1.0.0", "example-module/")