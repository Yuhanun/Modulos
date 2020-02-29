import os
import git

def clone_dependency(dir: str, name: str, version: str, dep_url: str):
    git.Git(f"{dir}.modulos/dependencies/{name}/{version}").clone(dep_url)

def get_local_repo_path(dir: str) -> str:
    return os.path.abspath(f"{dir}.modulos/modulos-index")

def clone_repo_local(dir: str = ".") -> str:
    """
    Clones the local repo into {dir}/.modulos/modulos-index

    :dir: Directory to clone into
    :return: The absolute path to git cache
    """
    git.Git(f"{dir}.modulos").clone("https://github.com/Yuhanun/modulos-index.git")
    return get_local_repo_path(dir)

def repo_local_exists(dir: str = ".") -> bool:
    """
    Checks if {dir}/.modulos/modulos-index exists
    """
    return os.path.isdir(get_local_repo_path(dir))

def pull_repo_local(dir: str = ".") -> str:
    """
    Pulls the local repo {dir}/.modulos/modulos-index

    :dir: Directory to clone into
    :return: The absolute path to git cache
    """
    print("Fetching modulos indexes...", end='')
    git.Repo(get_local_repo_path(dir)).remote().pull()
    print("\rFetched modulos indexes!   ")

def update_repo_local(dir: str = ".") -> str:
    if not repo_local_exists(dir):
        clone_repo_local(dir)
    pull_repo_local(dir)
    return get_local_repo_path(dir)
