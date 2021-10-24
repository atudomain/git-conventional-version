from typing import List
from git import Repo
from git_conventional_version.versioning.conventional import Conventional 
from git_conventional_version.versioning.versions import DevelopmentalVersion
from git_conventional_version.versioning.versions import FinalVersion
from git_conventional_version.versioning.versions import ReleaseCandidateVersion
from git_conventional_version.versioning.versions import Version
import re


class Release:
    version_class = Version

    def __init__(
        self,
        repo: Repo
    ) -> None:
        self.repo = repo 
        self.conventional = Conventional(self.repo)

    def get_old_version(self) -> Version:
        versions = self.get_versions()
        if len(versions) > 0:
            return self.version_class.from_tag(versions[0])
        else:
            return self.version_class()

    def get_new_version(self) -> Version:
        return self.conventional.increment(self.get_old_version())

    def get_versions(self) -> List[Version]:
        tags = [str(tag) for tag in self.repo.tags]
        versions = [tag for tag in tags if re.search(self.version_class.pattern, tag)]
        return sorted(
            versions,
            key=lambda x: tuple(re.findall(r'\d+', x)),
            reverse=True
        )

    def get_old_version_string(self) -> str:
        return str(self.get_old_version())

    def get_new_version_string(self) -> str:
        return str(self.get_new_version())

    def get_version_strings(self) -> str:
        return [str(x) for x in self.get_versions()]

    def get_local_version_string(self) -> str:
        sha = self.repo.head.commit.hexsha
        short_sha = self.repo.git.rev_parse(sha, short=4)
        return f"{self.get_old_version()}+{short_sha}"


class FinalRelease(Release):
    version_class = FinalVersion


class PreRelease(Release):
    def __init__(
        self,
        repo: Repo
    ) -> None:
        super().__init__(repo)
        self.final_release = FinalRelease(repo)
        
    def get_old_version(self) -> Version:
        pre_release_version = super().get_old_version()
        final_version = self.final_release.get_new_version()
        if pre_release_version.numbers[3] == 0 \
        or final_version.numbers != pre_release_version.numbers[:3]:
            pre_release_version = self.version_class(
                numbers=final_version.numbers + [0]
            )
        return pre_release_version

    def get_new_version(self) -> Version:
        pre_release_version = self.get_old_version()
        try:
            if self.repo.head.commit.hexsha \
            == self.repo.tag(pre_release_version).commit.hexsha:
                return pre_release_version
        except ValueError:
            pass
        pre_release_version.numbers[3] += 1
        return pre_release_version


class ReleaseCandidateRelease(PreRelease):
    version_class = ReleaseCandidateVersion


class DevelopmentalRelease(PreRelease):
    version_class = DevelopmentalVersion
