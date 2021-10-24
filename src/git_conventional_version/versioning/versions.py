from abc import abstractclassmethod
import re


class Version:
    pattern: str
    str_format: str

    def __init__(
        self,
        numbers: list = None
    ) -> None:
        self.numbers = numbers

    @classmethod
    def validate_tag(cls, tag: str) -> None:
        if not re.search(cls.pattern, tag):
            raise Exception(f"Tag {tag} does not match pattern {cls.pattern}.")

    @abstractclassmethod
    def _extract_version(cls, tag: str) -> "Version":
        groups = re.search(cls.pattern, tag).groups()
        return cls([int(group) for group in groups])

    @abstractclassmethod
    def from_tag(cls, tag: str) -> "Version":
        cls.validate_tag(tag)
        return cls._extract_version(tag)

    def __str__(self):
        return self.str_format % tuple(self.numbers)


class FinalVersion(Version):
    pattern: str = r"^(\d+)\.(\d+)\.(\d+)$"
    str_format: str = "%d.%d.%d"
    def __init__(self, numbers: list = None) -> None:
        super().__init__(numbers=numbers)
        if not numbers:
            self.numbers = [0, 0, 0]


class PreReleaseVersion(Version):
    def __init__(self, numbers: list = None) -> None:
        super().__init__(numbers=numbers)
        if not numbers:
            self.numbers = [0, 0, 0, 0]


class ReleaseCandidateVersion(PreReleaseVersion):
    pattern: str = r"^(\d+)\.(\d+)\.(\d+)rc(\d+)$"
    str_format: str = "%d.%d.%drc%d"


class DevelopmentalVersion(PreReleaseVersion):
    pattern: str = r"^(\d+)\.(\d+)\.(\d+)dev(\d+)$"
    str_format: str = "%d.%d.%ddev%d"
