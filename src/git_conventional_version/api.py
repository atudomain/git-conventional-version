from git_conventional_version.versioning.releases import DevelopmentalRelease
from git_conventional_version.versioning.releases import FinalRelease
from git_conventional_version.versioning.releases import Release
from git_conventional_version.versioning.releases import ReleaseCandidateRelease
from git import Repo


class InvalidReleaseTypeError(Exception):
    pass


def _create_release(type: str="final") -> Release:
    repo = Repo(search_parent_directories=True)
    if type == "final":
        release = FinalRelease(repo)
    elif type == "rc":
        release = ReleaseCandidateRelease(repo)
    elif type == "dev":
        release = DevelopmentalRelease(repo)
    else:
        raise Exception(f"Type: '{type}' is not valid.")
    return release


def get_old_version(type: str) -> str:
    return _create_release(type).get_old_version_string()


def get_new_version(type: str) -> str:
    return _create_release(type).get_new_version_string()


def get_local_version() -> str:
    return _create_release().get_local_version_string()
