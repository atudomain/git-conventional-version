import pytest
from git_conventional_version.versioning.releases import FinalRelease
from git_conventional_version.versioning.releases import ReleaseCandidateRelease


def test_get_version_string_empty_repo(git_repo):
    release_class = FinalRelease
    release = release_class(git_repo)
    old_version = release.get_old_version_string()
    assert old_version == "0.0.0"
    new_version = release.get_new_version_string()
    assert new_version == "0.0.0"


def test_get_version_string_tag_different_branch_repo(
    git_repo_tag_different_branch
):
    release_class = FinalRelease
    release = release_class(git_repo_tag_different_branch)
    new_version = release.get_new_version_string()
    assert new_version == "2.0.0"


def test_get_version_string_nontagged_repo(git_repo_nontagged):
    release_class = FinalRelease
    release = release_class(git_repo_nontagged)
    old_version = release.get_old_version_string()
    assert old_version == "0.0.0"
    new_version = release.get_new_version_string()
    assert new_version == "0.1.0"


def test_get_version_string_on_tagged_commit(git_repo_tagged_commit):
    release_class = FinalRelease
    release = release_class(git_repo_tagged_commit)
    old_version = release.get_old_version_string()
    assert old_version == "3.0.0"
    new_version = release.get_new_version_string()
    assert new_version == "3.0.0"


@pytest.mark.parametrize(
    "release_class,old_version_string,new_version_string",
    [
        (FinalRelease, "1.0.0", "1.1.0"),
        (ReleaseCandidateRelease, "1.1.0rc0", "1.1.0rc1")
    ]
)
def test_get_version_string_on_conventional_commit(
    git_repo_conventional_commit,
    release_class,
    old_version_string,
    new_version_string
):
    release = release_class(git_repo_conventional_commit)
    old_version = release.get_old_version_string()
    assert old_version == old_version_string
    new_version = release.get_new_version_string()
    assert new_version == new_version_string


def test_get_prerelease_version_string(git_repo_prerelease):
    release_class = ReleaseCandidateRelease
    release = release_class(git_repo_prerelease)
    old_version = release.get_old_version_string()
    assert old_version == "1.1.0rc0"
    new_version = release.get_new_version_string()
    assert new_version == "1.1.0rc1"


def test_get_next_prerelease_version_string(
    git_repo_next_prerelease
):
    release_class = ReleaseCandidateRelease
    release = release_class(git_repo_next_prerelease)
    new_version = release.get_new_version_string()
    assert new_version == "1.1.0rc2"


def test_get_next_tagged_prerelease_version_string(
    git_repo_tagged_prerelease
):
    release_class = ReleaseCandidateRelease
    release = release_class(git_repo_tagged_prerelease)
    new_version = release.get_new_version_string()
    assert new_version == "1.0.0rc3"
    old_version = release.get_old_version_string()
    assert old_version == "1.0.0rc3"
