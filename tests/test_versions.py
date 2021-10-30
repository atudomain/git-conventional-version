import pytest

from git_conventional_version.versioning.versions import \
    FinalVersion, \
    ReleaseCandidateVersion, \
    DevelopmentalVersion


@pytest.mark.parametrize(
    "version_class,numbers,valid_version,invalid_version",
    [
        (FinalVersion, [1,2,3], "1.2.3", "1.2"),
        (ReleaseCandidateVersion, [1,2,3,4], "1.2.3rc4", "1.2.3"),
        (DevelopmentalVersion, [1,2,3,4], "1.2.3dev4", "1.2.3.4", )
    ]
)
def test_version_classes(
    version_class, 
    numbers, 
    valid_version, 
    invalid_version
):
    version = version_class(numbers)
    assert str(version) == valid_version
    version_class._validate_tag(valid_version)
    with pytest.raises(Exception):
        version_class._validate_tag(invalid_version)
    version = version_class.from_tag(valid_version)
    assert str(version) == valid_version
