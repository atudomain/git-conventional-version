import pytest
from git import Repo


def _set_user(repo):
    repo.config_writer().set_value("user", "name", "example").release()
    repo.config_writer().set_value("user", "email", "example@example.com").release()


@pytest.fixture()
def repo(tmpdir):
    repo = Repo.init(tmpdir)
    _set_user(repo)
    yield repo
