from git_conventional_version.api import get_local_version
from git_conventional_version.api import get_new_version
from git_conventional_version.api import get_old_version
import argparse
import sys


def cli():
    parser = argparse.ArgumentParser(
        description="Print automatically bumped version based on git tags and messages."
    )
    parser.add_argument(
        "-t", "--type",
        required=False,
        default="final",
        choices=["final", "rc", "dev", "local"],
        type=str,
        help="Choose type of version."
    )
    parser.add_argument(
        "--old",
        required=False,
        action='store_true',
        default=False,
        help="Print current (old) version instead."
    )
    args = parser.parse_args()
    if args.type == "local":
        print(get_local_version())
    elif args.old:
        print(get_old_version(type=args.type))
    else:
        print(get_new_version(type=args.type))
    sys.exit(0)


if __name__ == "__main__":
    cli()
