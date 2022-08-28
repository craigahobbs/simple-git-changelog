# simple-git-changelog

[![PyPI - Status](https://img.shields.io/pypi/status/simple-git-changelog)](https://pypi.org/project/simple-git-changelog/)
[![PyPI](https://img.shields.io/pypi/v/simple-git-changelog)](https://pypi.org/project/simple-git-changelog/)
[![GitHub](https://img.shields.io/github/license/craigahobbs/simple-git-changelog)](https://github.com/craigahobbs/simple-git-changelog/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/simple-git-changelog)](https://pypi.org/project/simple-git-changelog/)

**simple-git-changelog** is a command-line tool for creating and updating a git project's changelog
file.

To create your project's changelog file, run simple-git-changelog in your project's root directory:

``` sh
$ simple-git-changelog
```

By default, the "CHANGELOG.md" file is created with your project's changes. For example:

``` markdown
# Changelog

## 2021-04-30

- [abcdf0](https://github.com/username/project-name/commit/abcdf0) most recent change

- [abcdef](https://github.com/username/project-name/commit/abcdef) previous change
```

Edit "CHANGELOG.md" as appropriate and commit. To update your changelog file later, simply run
simple-git-changelog again. Change items for new git changes are added to the top of the changelog:

``` markdown
# MyProject Changelog

## 2021-05-01

- [abcdf1](https://github.com/username/project-name/commit/abcdf1) one more thing

## 2021-04-30

- [abcdf0](https://github.com/username/project-name/commit/abcdf0) most recent change

- [abcdef](https://github.com/username/project-name/commit/abcdef) previous change
```


## Usage

```
usage: simple-git-changelog [-h] [-o FILE]

options:
  -h, --help  show this help message and exit
  -o FILE     specify the change log file (default is "CHANGELOG.md")
```

## Development

This project is developed using [python-build](https://github.com/craigahobbs/python-build#readme). It was started
using [python-template](https://github.com/craigahobbs/python-template#readme) as follows:

```
template-specialize python-template/template/ simple-git-changelog/ -k package simple-git-changelog -k name 'Craig A. Hobbs' -k email 'craigahobbs@gmail.com' -k github 'craigahobbs' -k noapi 1
```
