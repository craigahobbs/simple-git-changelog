# Licensed under the MIT License
# https://github.com/craigahobbs/simple-git-changelog/blob/main/LICENSE

"""
simple-git-changelog command-line script main module
"""

import argparse
from datetime import date
import os
import re
import subprocess


def main(args=None):
    """
    simple-git-changelog command-line script main entry point
    """

    # Command-line arguments
    parser = argparse.ArgumentParser(prog='simple-git-changelog')
    parser.add_argument('-o', metavar='FILE', dest='output', default='CHANGELOG.md',
                        help='specify the change log file (default is "CHANGELOG.md")')
    args = parser.parse_args(args=args)

    # Parse the change log file, if any
    if os.path.isfile(args.output):
        with open(args.output, 'r', encoding='utf-8') as changelog_file:
            all_lines = list(changelog_file)
            title_line = next(iter(line for line in all_lines if line.startswith('# ')), '# Changelog\n')
            changelog_lines = list(line for line in all_lines if not line.startswith('# '))
        changelog_commits = parse_changelog(changelog_lines)
    else:
        title_line = '# Changelog\n'
        changelog_lines = []
        changelog_commits = set()

    # Any new changes?
    git_changes = get_git_changes()
    if git_changes and git_changes[0][0] not in changelog_commits:
        git_url = get_git_url()

        # Write the updated changelog file
        with open(args.output, 'w', encoding='utf-8') as changelog_file:

            # Write the changelog title
            changelog_file.write(title_line)

            # Write entries for new changes
            changelog_file.write(f'\n## {date.today().isoformat()}\n')
            for commit, subject in git_changes:
                if commit in changelog_commits:
                    break
                changelog_file.write(f'\n- [{commit}]({git_url}/commit/{commit}) - {escape_markdown_span(subject)}\n')

            # Write pre-existing changelog lines
            if changelog_lines and changelog_lines[0] != '\n':
                changelog_file.write('\n')
            for changelog_line in changelog_lines:
                changelog_file.write(changelog_line)


# Helper function to escape Markdown span characters
def escape_markdown_span(text):
    return re_escape_markdown_span.sub(r'\\\1', text)

re_escape_markdown_span = re.compile(r'([\\\[\]()*])')


def parse_changelog(lines):
    commits = set()
    for line in lines:
        change_match = re_change.search(line)
        if change_match is not None:
            commits.add(change_match.group('commit'))
    return commits

re_change = re.compile(r'^-\s+\[(?P<commit>[0-9a-f]+)\]')


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
