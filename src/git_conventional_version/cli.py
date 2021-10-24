from git_conventional_version.api import Api 
from git_conventional_version.api import version_types
from git import Repo
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
        choices=version_types,
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
    api = Api(repo=Repo(search_parent_directories=True))
    if args.type == "local":
        print(api.get_local_version())
    elif args.old:
        print(api.get_old_version(type=args.type))
    else:
        print(api.get_new_version(type=args.type))
    sys.exit(0)


if __name__ == "__main__":
    cli()
