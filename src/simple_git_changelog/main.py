# Licensed under the MIT License
# https://github.com/craigahobbs/simple-git-changelog/blob/main/LICENSE

import argparse
from datetime import date
import os
import re
import subprocess

from . import __version__ as VERSION


def main(args=None):

    # Command-line arguments
    parser = argparse.ArgumentParser(prog='simple-git-changelog')
    parser.add_argument('-o', metavar='FILE', dest='output', default='CHANGELOG.md',
                        help='specify the change log file (default is "CHANGELOG.md")')
    parser.add_argument('--version', action='store_true',
                        help='show version number and quit')
    args = parser.parse_args(args=args)
    if args.version:
        parser.exit(message=VERSION + '\n')

    # Parse the change log file, if any
    if os.path.isfile(args.output):
        with open(args.output, 'r') as changelog_file:
            changelog_lines = list(changelog_file)
        changelog_commits = parse_changelog(changelog_lines)
    else:
        changelog_commits = set()
        changelog_lines = []

    # Any new changes?
    git_changes = get_git_changes()
    if git_changes and git_changes[0][0] not in changelog_commits:
        git_url = get_git_url()

        # Write the updated changelog file
        with open(args.output, 'w') as changelog_file:

            # Write entries for new changes
            changelog_file.write(f'## {date.today().isoformat()}\n')
            for commit, subject in git_changes:
                if commit in changelog_commits:
                    break
                changelog_file.write(f'\n- [{commit}]({git_url}/commit/{commit}) - {subject}\n')

            # Write pre-existing changelog lines
            if changelog_lines:
                changelog_file.write('\n')
            for changelog_line in changelog_lines:
                changelog_file.write(changelog_line)


def parse_changelog(lines):
    re_change = re.compile(r'^-\s+\[(?P<commit>[0-9a-f]+)\]')
    commits = set()
    for line in lines:
        change_match = re_change.search(line)
        if change_match is not None:
            commits.add(change_match.group('commit'))
    return commits


def get_git_changes():
    commits = subprocess.check_output(['git', 'log', '--pretty=format:%h %s'], encoding='utf-8')
    return [line.split(' ', 1) for line in commits.splitlines()]


def get_git_url():
    git_origin = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], encoding='utf-8').strip()
    git_url = re.sub(r'\.git$', '', git_origin)
    git_url_match = re.search(r'^git@(?P<domain>[^:]+):(?P<user>[^/]+)/(?P<project>.+)$', git_url)
    if git_url_match is not None:
        git_url = f'https://{git_url_match.group("domain")}/{git_url_match.group("user")}/{git_url_match.group("project")}'
    return git_url
