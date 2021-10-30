# GIT-CONVENTIONAL-VERSION

![ci-badge](https://github.com/atudomain/git-conventional-version/actions/workflows/github-actions.yml/badge.svg?branch=main)

Find version automatically based on git tags and commit messages.

The tool is very specific in its function, so it is very flexible. 

You can use it as a part of many different integrations and it will not break your process.

## Install

```
python3 -m pip install git-conventional-version
```

## Usage

Get new bumped final version:
```
gcv
```

Get new bumped release candidate version:
```
gcv --type=rc
```

Get current (old) version, 0.0.0 if none exists:
```
gcv --old
```

Example of CI automation script:
```
old=$(gcv --old)
new=$(gcv)
# check if version bump would happen
if [ ! $new == $old ]; then
    # if yes, update setup.cfg
    sed -i "s/^version.*/version = $new/g" setup.cfg
    # and commit release
    git add setup.cfg
    git commit -m "$new"
    git tag "$new"
    git push --tags
    git push
fi
```

## Version formats

Tags are equivalent to versions, no suffix or prefix is added or interpreted.
Formats follow https://www.python.org/dev/peps/pep-0440/.

- Final version

Standard tag is in the format `\d+\.\d+\.d+` ie. `1.0.0`. It can be divided into `major` . `minor` . `patch` versions.

It is automatically bumped based on commits messages and old version of the same type (look at `Git commit message convention` below).

- Pre-release versions

Pre-release versions bumps are calculated based on last final version, its expected bump and old version of the same pre-release type.

-    - Release candidate version

Format `\d+\.\d+\.d+rc\d+` ie. `1.0.0rc1`.

-    - Developmental version 

Format `\d+\.\d+\.d+dev\d+` ie. `1.0.0dev1`.

-    - Alpha version 

Format `\d+\.\d+\.d+a\d+` ie. `1.0.0a1`.

-    - Beta version 

Format `\d+\.\d+\.d+b\d+` ie. `1.0.0b1`.

- Local version

Also, local version can be created from commit sha and old version: `\d+\.\d+\.d\+.+` ie. `0.0.0+79ad`.

## Git commit message convention

Convention is based on https://www.conventionalcommits.org/en/v1.0.0/ (it's good!).
At the moment, only the following rules apply (I usually use only these but more can be added easily):
- Start commit with 'fix:' or 'fix(.*):' to bump patch version.
- Start commit with 'feat:' or 'feat(.*):' to bump minor version.
- Include in the commit line with 'breaking change:' to bump major version.

## Automatic changelog

On branch where your version tags are present, you can generate changelog:
```
gcv-log
```
Full changelog is generated and printed to stdout. You can redirect it to a file.
Assumes that you are about to release next version if not on commit with final version.

## Notices

Automatically handling many types of version tags in git is more complicated than it initially seems like.
