import pytest
import pathlib
import os
from git import Repo
from git_conventional_version.api import Api


def _commit_file(repo: Repo, filename: str, message: str) -> None:
    filepath = os.path.join(repo.working_dir, filename)
    pathlib.Path(filepath).touch()
    repo.git.add(".")
    repo.git.commit("-m", message)


def _compare_versions(repo, version_type, old_version, new_version):
    api = Api(repo)
    version = api.get_old_version(version_type)
    assert version == old_version
    version = api.get_new_version(version_type)
    assert version == new_version
    
    
@pytest.mark.parametrize(
    "version_type,old_version,new_version",
    [
        ("final", "0.0.0", "0.0.0"),
        ("rc", "0.0.0rc0", "0.0.0rc1"),
        ("dev", "0.0.0dev0", "0.0.0dev1")
    ]
)
def test_repo_empty(
    repo,
    version_type,
    old_version,
    new_version
):
    _compare_versions(repo, version_type, old_version, new_version)
    

@pytest.mark.parametrize(
    "version_type,old_version,new_version",
    [
        ("final", "1.0.0", "2.0.0"),
        ("rc", "2.0.0rc0", "2.0.0rc1"),
        ("dev", "2.0.0dev0", "2.0.0dev1")
    ]
)
def test_repo_tag_on_different_branch(
    repo,
    version_type,
    old_version,
    new_version
):
    _commit_file(repo, "testfile1.txt", "feat(test): add test file")
    repo.git.checkout("-b", "development")
    _commit_file(repo, "testfile2.txt", "breaking change: add test file")
    repo.git.checkout("master")
    _commit_file(repo, "testfile3.txt", "1.0.0")
    repo.create_tag("1.0.0")
    repo.git.checkout("development")

    _compare_versions(repo, version_type, old_version, new_version)


@pytest.mark.parametrize(
    "version_type,old_version,new_version",
    [
        ("final", "0.0.0", "0.1.0"),
        ("rc", "0.1.0rc0", "0.1.0rc1"),
        ("dev", "0.1.0dev0", "0.1.0dev1")
    ]
)
def test_repo_with_commit_without_tags(
    repo,
    version_type,
    old_version,
    new_version
):
    _commit_file(repo, "testfile1.txt", "feat(test): add test file")

    _compare_versions(repo, version_type, old_version, new_version)


@pytest.mark.parametrize(
    "version_type,old_version,new_version",
    [
        ("final", "3.0.0", "3.0.0"),
        ("rc", "3.0.0rc0", "3.0.0rc1"),
        ("dev", "3.0.0dev0", "3.0.0dev1")
    ]
)
def test_repo_with_commits_tagged_final(
    repo,
    version_type,
    old_version,
    new_version
):
    _commit_file(repo, "testfile1.txt", "breaking change: test")
    repo.create_tag("1.0.0")
    _commit_file(repo, "testfile2.txt", "breaking change: test 2")
    repo.create_tag("2.0.0")
    _commit_file(repo, "testfile3.txt", "breaking change: test 3")
    repo.create_tag("3.0.0")

    _compare_versions(repo, version_type, old_version, new_version)


@pytest.mark.parametrize(
    "version_type,old_version,new_version",
    [
        ("final", "1.0.0", "1.1.0"),
        ("rc", "1.1.0rc0", "1.1.0rc1"),
        ("dev", "1.1.0dev0", "1.1.0dev1")
    ]
)
def test_repo_with_final_tag_and_conventional_commit(
    repo,
    version_type,
    old_version,
    new_version
):
    _commit_file(repo, "testfile1.txt", "feat(test): add test file")
    repo.create_tag("1.0.0")
    _commit_file(repo, "testfile2.txt", "feat(test): add another file")

    _compare_versions(repo, version_type, old_version, new_version)


@pytest.mark.parametrize(
    "version_type,old_version,new_version",
    [
        ("final", "1.0.0", "1.1.0"),
        ("rc", "1.1.0rc0", "1.1.0rc1"),
        ("dev", "1.1.0dev0", "1.1.0dev1")
    ]
)
def test_repo_with_rc_tag_and_conventional_commit(
    repo,
    version_type,
    old_version,
    new_version
):
    _commit_file(repo, "testfile1.txt", "feat(test): add test file")
    repo.create_tag("1.0.0")
    repo.create_tag("1.0.0rc1")
    _commit_file(repo, "testfile2.txt", "feat(test): add another file")

    _compare_versions(repo, version_type, old_version, new_version)


@pytest.mark.parametrize(
    "version_type,old_version,new_version",
    [
        ("final", "0.0.0", "1.0.0"),
        ("rc", "1.0.0rc3", "1.0.0rc3"),
        ("dev", "1.0.0dev0", "1.0.0dev1")
    ]
)
def test_repo_with_many_rc_tags(
    repo,
    version_type,
    old_version,
    new_version
):
    _commit_file(repo, "testfile1.txt", "breaking change: whatever")
    repo.create_tag("1.0.0rc1")
    _commit_file(repo, "testfile2.txt", "breaking change: whatever 2")
    repo.create_tag("1.0.0rc2")
    _commit_file(repo, "testfile3.txt", "breaking change: whatever 3")
    repo.create_tag("1.0.0rc3")

    _compare_versions(repo, version_type, old_version, new_version)


@pytest.mark.parametrize(
    "version_type,old_version,new_version",
    [
        ("final", "1.0.0", "1.1.0"),
        ("rc", "1.1.0rc1", "1.1.0rc2"),
        ("dev", "1.1.0dev0", "1.1.0dev1")
    ]
)
def test_repo_with_rc_tag_since_final_tag(
    repo,
    version_type,
    old_version,
    new_version
):
    _commit_file(repo, "testfile1.txt", "feat(test): add test file")
    repo.create_tag("1.0.0")
    _commit_file(repo, "testfile2.txt", "feat(test): add another file")
    repo.create_tag("1.1.0rc1")
    _commit_file(repo, "testfile3.txt", "feat(test): add another file")

    _compare_versions(repo, version_type, old_version, new_version)
