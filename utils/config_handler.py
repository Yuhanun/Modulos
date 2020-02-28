import os
import toml

"""
File format:
[project]
name = "{name}"
version = "MAJOR.MINOR.PATCH"
authors = ["FIRSTNAME LATNAME <email@email.ext>"]
ouput_folder = "bin"

[settings]
cpp_version = "17"
compiler = "/path/to/compiler"
Wall = 1
Wextra = 1
exclude_errors = ["no-return"]

[dependencies]
nlohmann-json = "1.0.0"
cpr = "1.0.3"

[exclude]
directories = ["./path"]
files = ["./test.cpp"]
"""


def is_module(directory: str) -> str:
    return os.path.isfile(f"{directory}/modulos.toml")


def get_output_path(directory: str, create: bool = True, add_binary: bool = True) -> str:
    """
    Gets output path from {directory}/modulos.toml

    :directory: Directory to get the toml from
    :create: Whether to create the output directory or not if it doesn't exist yet
    """

    valid, config = load_config(directory)

    if not valid:
        return

    project = config.get("project", {})

    if len(project.keys()) == 0:
        return

    output_dir = os.path.abspath(
        directory + project.get("output_folder", "bin"))

    if not os.path.isdir(output_dir):
        if not create:
            return
        os.makedirs(output_dir)

    return output_dir + (("/" + get_name(directory) + ".out") if add_binary else "")


def get_name(directory: str) -> str:
    """
    Gets the name from {directory}/modulos.toml

    :directory: Directory to get the toml from
    """

    valid, config = load_config(directory)

    if not valid:
        return

    project = config.get("project", {})

    if len(project.keys()) == 0:
        return

    return project.get('name')

def get_compiler(directory: str) -> str:
    """
    Gets compiler from {directory}/modulos.toml

    :directory: Directory to get the toml from
    """

    valid, config = load_config(directory)

    if not valid:
        return

    return config.get('settings', {}).get('compiler')


def load_config(current_dir: str = "") -> (bool, dict):
    """
    Loads a moduls config, from file modulos.toml in current dir

    :current_dir: Directory to search in
    :return: Tuple with status and toml result
    False if file not found, True + dict if found
    """
    if not os.path.isfile(f"{current_dir}modulos.toml"):
        return False, {}

    return True, toml.load(f"{current_dir}modulos.toml")


def init_config(dir: str = ".", name: str = "", compiler: str = "", version: str = "", folder: str = ".") -> (bool, str):
    """
    Creates a modulos module

    :dir: Directory to create it in
    :name: Name of binary
    :compiler: Compiler to use
    :version: C++ version, such as `17`
    :folder: folder to init into
    """

    dir = os.path.abspath(dir)

    if not os.path.isdir(dir):
        os.mkdir(dir)

    toml_path = f"{dir}/modulos.toml"

    if os.path.isfile(toml_path):
        return False, f"Directory {dir} already contains a modulos.toml"

    if os.path.isdir(f"{dir}/src"):
        return False, f"Directory {dir} already contains ./src"

    if os.path.isdir(f"{dir}/src"):
        return False, f"Directory {dir} already contains ./include"

    if os.path.isdir(f"{dir}/.modulos"):
        return False, f"Directory {dir} already contains ./.modulos"

    os.mkdir(f"{dir}/src")
    os.mkdir(f"{dir}/include")
    os.makedirs(f"{dir}/.modulos/dependencies")
    with open(f"{dir}/.modulos/dependencies/dependencies.json", "a") as file:
        file.write("{}")

    # os.makedirs(f"{dir}/.modulos/history")

    with open(f"{dir}/src/main.cpp", "a") as file:
        file.write("""#include <iostream>

int main() {
    std::cout << "Hello World!" << std::endl;
    return 0;
}""")

    structure = {
        "project": {
            "name": name,
            "version": "1.0.0",
            "authors": [],
            "output_folder": "bin"
        },
        "settings": {
            "cpp_version": version,
            "compiler": compiler
        },
        "dependencies": {},
        "exclude": {}
    }

    toml.dump(structure, open(toml_path, "a"))
    return True, f"Created {toml_path}"
