import pytest
from py._path.local import LocalPath
from git import Repo


@pytest.fixture(scope="session")
def git_repo(tmpdir_factory):
    path = tmpdir_factory.mktemp("repo")
    yield Repo.init(path)


def _commit_file(repo: Repo, path: LocalPath, filename: str, message: str) -> None:
    filepath = path / filename
    filepath.write_text("", encoding="utf-8")
    repo.git.add(".")
    repo.git.commit("-m", message)


def _set_user(repo):
    repo.config_writer().set_value("user", "name", "example").release()
    repo.config_writer().set_value("user", "email", "example@example.com").release()


@pytest.fixture(scope="session")
def git_repo_nontagged(tmpdir_factory):
    path = tmpdir_factory.mktemp("repo_nontagged")
    repo = Repo.init(path)
    _set_user(repo)
    _commit_file(repo, path, "testfile1.txt", "feat(test): add test file")
    yield repo


@pytest.fixture(scope="session")
def git_repo_tag_different_branch(tmpdir_factory):
    path = tmpdir_factory.mktemp("repo_tag_different_branch")
    repo = Repo.init(path)
    _set_user(repo)
    _commit_file(repo, path, "testfile1.txt", "feat(test): add test file")
    repo.git.checkout("-b", "development")
    _commit_file(repo, path, "testfile2.txt", "breaking change: add test file")
    repo.git.checkout("master")
    _commit_file(repo, path, "testfile3.txt", "1.0.0")
    repo.create_tag("1.0.0")
    repo.git.checkout("development")
    yield repo


@pytest.fixture(scope="session")
def git_repo_tagged_commit(tmpdir_factory):
    path = tmpdir_factory.mktemp("repo_tagged_commit")
    repo = Repo.init(path)
    _set_user(repo)
    _commit_file(repo, path, "testfile1.txt", "feat(test): add test file")
    repo.create_tag("1.0.0")
    yield repo


@pytest.fixture(scope="session")
def git_repo_conventional_commit(tmpdir_factory):
    path = tmpdir_factory.mktemp("repo_conventional_commit")
    repo = Repo.init(path)
    _set_user(repo)
    _commit_file(repo, path, "testfile1.txt", "feat(test): add test file")
    repo.create_tag("1.0.0")
    _commit_file(repo, path, "testfile2.txt", "feat(test): add another file")
    yield repo


@pytest.fixture(scope="session")
def git_repo_prerelease(tmpdir_factory):
    path = tmpdir_factory.mktemp("repo_prerelease")
    repo = Repo.init(path)
    _set_user(repo)
    _commit_file(repo, path, "testfile1.txt", "feat(test): add test file")
    repo.create_tag("1.0.0")
    repo.create_tag("1.0.0rc1")
    _commit_file(repo, path, "testfile2.txt", "feat(test): add another file")
    yield repo


@pytest.fixture(scope="session")
def git_repo_next_prerelease(tmpdir_factory):
    path = tmpdir_factory.mktemp("repo_next_prerelease")
    repo = Repo.init(path)
    _set_user(repo)
    _commit_file(repo, path, "testfile1.txt", "feat(test): add test file")
    repo.create_tag("1.0.0")
    _commit_file(repo, path, "testfile2.txt", "feat(test): add another file")
    repo.create_tag("1.1.0rc1")
    _commit_file(repo, path, "testfile3.txt", "feat(test): add another file")
    yield repo
