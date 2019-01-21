# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from logging import getLogger
from pathlib import Path
from urllib.parse import urlparse

from frambo.utils import run_cmd

logger = getLogger(__name__)


class Git(object):
    """Class for working with git."""

    @staticmethod
    def call_git_cmd(cmd, return_output=True, msg=None, git_dir=None, shell=True):
        """
        Runs the GIT command with specified arguments
        :param cmd: list or string, git subcommand for execution
        :param return_output: bool, return output of the command ?
        :param msg: log this before running the command
        :param git_dir: run the command in another directory
        :param shell: bool, run git commands in shell by default
        :return: output of the git command
        """
        if msg:
            logger.info(msg)

        command = 'git'
        # use git_dir as work-tree git parameter and git-dir parameter (with added git.postfix)
        if git_dir:
            command += f" --git-dir {git_dir}/.git"
            command += f" --work-tree {git_dir}"
        if isinstance(cmd, str):
            command += f" {cmd}"
        elif isinstance(cmd, list):
            command += f" {' '.join(cmd)}"
        else:
            raise ValueError(f"{cmd} is not a list nor a string")

        output = run_cmd(command, return_output=return_output, shell=shell)
        logger.debug(output)
        return output

    @staticmethod
    def parse_git_repo(potential_url):
        """Cover the following variety of URL forms for Github/Gitlab repo referencing.

        1) www.domain.com/foo/bar
        2) (same as above, but with ".git" in the end)
        3) (same as the two above, but without "www.")
        # all of the three above, but starting with "http://", "https://", "git://", "git+https://"
        4) git@domain.com:foo/bar
        5) (same as above, but with ".git" in the end)
        6) (same as the two above but with "ssh://" in front or with "git+ssh" instead of "git")

        Returns a tuple (<username>, <reponame>) or None if this does not seem to be a Github repo.

        Notably, the repo *must* have exactly username and reponame, nothing else and nothing
        more. E.g. `github.com/<username>/<reponame>/<something>` is *not* recognized.
        """
        if not potential_url:
            return None

        # transform 4-6 to a URL-like string, so that we can handle it together with 1-3
        if '@' in potential_url:
            split = potential_url.split('@')
            if len(split) == 2:
                potential_url = 'http://' + split[1]
            else:
                # more @s ?
                return None

        # make it parsable by urlparse if it doesn't contain scheme
        if not potential_url.startswith(('http://', 'https://', 'git://', 'git+https://')):
            potential_url = 'http://' + potential_url

        # urlparse should handle it now
        parsed = urlparse(potential_url)

        username = None
        if ':' in parsed.netloc:
            # e.g. domain.com:foo or domain.com:1234, where foo is username, but 1234 is port number
            split = parsed.netloc.split(':')
            if split[1] and not split[1].isnumeric():
                username = split[1]

        # path starts with '/', strip it away
        path = parsed.path.lstrip('/')

        # strip trailing '.git'
        if path.endswith('.git'):
            path = path[:-len('.git')]

        split = path.split('/')
        if username and len(split) == 1:
            # path contains only reponame, we got username earlier
            return username, path
        if not username and len(split) == 2:
            # path contains username/reponame
            return split[0], split[1]

        # all other cases
        return None

    @staticmethod
    def get_username_from_git_url(url):
        """http://github.com/foo/bar.git -> foo"""
        user_repo = Git.parse_git_repo(url)
        return user_repo[0] if user_repo else None

    @staticmethod
    def get_reponame_from_git_url(url):
        """http://github.com/foo/bar.git -> bar"""
        user_repo = Git.parse_git_repo(url)
        return user_repo[1] if user_repo else None

    @staticmethod
    def strip_dot_git(url):
        """Strip trailing .git"""
        return url[:-len('.git')] if url.endswith('.git') else url

    @staticmethod
    def create_dot_gitconfig(user_name, user_email):
        """
        Create ~/.gitconfig file.
        :param user_name: git user name
        :param user_email: git user email
        """

        content = f"""[user]
\tname = {user_name}
\temail = {user_email}
[remote "origin"]
\tfetch = +refs/pull/*/head:refs/remotes/origin/pr/*
"""
        (Path.home() / '.gitconfig').write_text(content)
