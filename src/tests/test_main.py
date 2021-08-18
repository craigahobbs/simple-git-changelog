# Licensed under the MIT License
# https://github.com/craigahobbs/simple-git-changelog/blob/main/LICENSE

import datetime
from io import StringIO
import os
import tempfile
import unittest
from unittest.mock import call, patch

from simple_git_changelog.__main__ import main as main_import
from simple_git_changelog.main import main


TEST_GIT_URL = 'git@github.com:craigahobbs/simple-git-changelog.git'
TEST_GIT_URL_HTTPS = 'https://github.com/craigahobbs/simple-git-changelog.git'


class TestMain(unittest.TestCase):

    def test_main_import(self):
        self.assertIs(main, main_import)

    def test_output(self):
        with patch('sys.stdout', StringIO()) as stdout, \
             patch('sys.stderr', StringIO()) as stderr, \
             tempfile.TemporaryDirectory() as tempdir, \
             patch('simple_git_changelog.main.date') as mock_date, \
             patch('subprocess.check_output', side_effect=[
                 '''\
abcdf0 this is a change
abcdef this is another change
''',
                 TEST_GIT_URL,
                 '''\
abcdf0 this is a change
abcdef this is another change
''',
                 '''\
abcdf1 one more thing
abcdf0 this is a change
abcdef this is another change
''',
                 TEST_GIT_URL
             ]) as check_output:
            output_filename = os.path.join(tempdir, 'CHANGELOG.md')

            # Create file
            mock_date.today.return_value = datetime.date(2021, 4, 30)
            main(['-o', output_filename])
            with open(output_filename, 'r') as output_file:
                self.assertEqual(output_file.read(), '''\
## 2021-04-30

- [abcdf0](https://github.com/craigahobbs/simple-git-changelog/commit/abcdf0) - this is a change

- [abcdef](https://github.com/craigahobbs/simple-git-changelog/commit/abcdef) - this is another change
''')

            # Update file - nothing new
            mock_date.today.return_value = datetime.date(2021, 5, 1)
            main(['-o', output_filename])
            with open(output_filename, 'r') as output_file:
                self.assertEqual(output_file.read(), '''\
## 2021-04-30

- [abcdf0](https://github.com/craigahobbs/simple-git-changelog/commit/abcdf0) - this is a change

- [abcdef](https://github.com/craigahobbs/simple-git-changelog/commit/abcdef) - this is another change
''')

            # Update file
            mock_date.today.return_value = datetime.date(2021, 5, 1)
            main(['-o', output_filename])
            with open(output_filename, 'r') as output_file:
                self.assertEqual(output_file.read(), '''\
## 2021-05-01

- [abcdf1](https://github.com/craigahobbs/simple-git-changelog/commit/abcdf1) - one more thing

## 2021-04-30

- [abcdf0](https://github.com/craigahobbs/simple-git-changelog/commit/abcdf0) - this is a change

- [abcdef](https://github.com/craigahobbs/simple-git-changelog/commit/abcdef) - this is another change
''')

        self.assertEqual(stdout.getvalue(), '')
        self.assertEqual(stderr.getvalue(), '')
        self.assertListEqual(
            check_output.mock_calls,
            [
                call(['git', 'log', '--pretty=format:%h %s'], encoding='utf-8'),
                call(['git', 'config', '--get', 'remote.origin.url'], encoding='utf-8'),
                call(['git', 'log', '--pretty=format:%h %s'], encoding='utf-8'),
                call(['git', 'log', '--pretty=format:%h %s'], encoding='utf-8'),
                call(['git', 'config', '--get', 'remote.origin.url'], encoding='utf-8')
            ]
        )

    def test_unmatched_git_url(self):
        with patch('sys.stdout', StringIO()) as stdout, \
             patch('sys.stderr', StringIO()) as stderr, \
             tempfile.TemporaryDirectory() as tempdir, \
             patch('simple_git_changelog.main.date') as mock_date, \
             patch('subprocess.check_output', side_effect=[
                 '''\
abcdf0 this is a change
abcdef this is another change
''',
                 TEST_GIT_URL_HTTPS
             ]) as check_output:
            output_filename = os.path.join(tempdir, 'CHANGELOG.md')

            # Create file
            mock_date.today.return_value = datetime.date(2021, 4, 30)
            main(['-o', output_filename])
            with open(output_filename, 'r') as output_file:
                self.assertEqual(output_file.read(), '''\
## 2021-04-30

- [abcdf0](https://github.com/craigahobbs/simple-git-changelog/commit/abcdf0) - this is a change

- [abcdef](https://github.com/craigahobbs/simple-git-changelog/commit/abcdef) - this is another change
''')

        self.assertEqual(stdout.getvalue(), '')
        self.assertEqual(stderr.getvalue(), '')
        self.assertListEqual(
            check_output.mock_calls,
            [
                call(['git', 'log', '--pretty=format:%h %s'], encoding='utf-8'),
                call(['git', 'config', '--get', 'remote.origin.url'], encoding='utf-8')
            ]
        )
