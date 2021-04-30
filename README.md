# simple-git-changelog

![PyPI - Status](https://img.shields.io/pypi/status/simple-git-changelog)
![PyPI](https://img.shields.io/pypi/v/simple-git-changelog)
![GitHub](https://img.shields.io/github/license/craigahobbs/simple-git-changelog)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/simple-git-changelog)

**simple-git-changelog** is a command-line tool for creating and updating a git project's changelog
file.

To create your project's changelog file, run simple-git-changelog in your project's root directory:

``` sh
$ simple-git-changelog
```

By default, the "CHANGELOG.md" file is created with your project's changes. For example:

``` markdown
## 2021-04-30

- [abcdf0](https://github.com/username/project-name/commit/abcdf0) most recent change

- [abcdef](https://github.com/username/project-name/commit/abcdef) previous change
```

Edit "CHANGELOG.md" as appropriate and commit. To update your changelog file later, simply run
simple-git-changelog again. Change items for new git changes are added to the top of the changelog:

``` markdown
## 2021-05-01

- [abcdf1](https://github.com/username/project-name/commit/abcdf1) one more thing

## 2021-04-30

- [abcdf0](https://github.com/username/project-name/commit/abcdf0) most recent change

- [abcdef](https://github.com/username/project-name/commit/abcdef) previous change
```


## Links

- [Package on pypi](https://pypi.org/project/simple-git-changelog/)
- [Source code on GitHub](https://github.com/craigahobbs/simple-git-changelog)


## Usage

```
usage: simple-git-changelog [-h] [-o FILE] [--version]

options:
  -h, --help  show this help message and exit
  -o FILE     specify the change log file (default is "CHANGELOG.md")
  --version   show version number and quit
```

## Development

This project is developed using [Python Build](https://github.com/craigahobbs/python-build#readme).
