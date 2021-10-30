import subprocess
import pytest
from git_conventional_version.api import version_types


commands = tuple(
    [
        f"gcv -t {version_type} {old}" 
        for version_type in version_types 
        for old in ("--old", "")
    ]
)


@pytest.mark.parametrize(
    "command",
    commands
)
def test_gcv(repo, command):
    subprocess.run(command, cwd=repo.working_dir, shell=True)


def test_gcv_log(repo):
    subprocess.run("gcv-log", cwd=repo.working_dir, shell=True)
