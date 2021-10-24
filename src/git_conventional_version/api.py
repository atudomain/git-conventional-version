from git_conventional_version.versioning.releases import DevelopmentalRelease
from git_conventional_version.versioning.releases import FinalRelease
from git_conventional_version.versioning.releases import Release
from git_conventional_version.versioning.releases import ReleaseCandidateRelease
from git import Repo


version_types = ["final", "rc", "dev", "local"]


class InvalidVersionTypeError(Exception):
    pass


class Api:
    def __init__(
        self,
        repo: Repo
    ) -> None:
        self.repo = repo

    def _create_release(self, type: str="final") -> Release:
        if type == "final":
            release = FinalRelease(self.repo)
        elif type == "rc":
            release = ReleaseCandidateRelease(self.repo)
        elif type == "dev":
            release = DevelopmentalRelease(self.repo)
        else:
            raise Exception(f"Type: '{type}' is not valid.")
        return release

    def get_old_version(self, type: str) -> str:
        return self._create_release(type).get_old_version_string()

    def get_new_version(self, type: str) -> str:
        return self._create_release(type).get_new_version_string()

    def get_local_version(self) -> str:
        return self._create_release().get_local_version_string()
