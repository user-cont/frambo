"""Test Git class."""

from subprocess import CalledProcessError
from os.path import isdir, isfile, join
import pytest

from frambo.git import Git


class TestGit(object):
    """Test Git class."""

    def test_call_git_cmd(self):
        assert Git.call_git_cmd("version").startswith("git version")

    @pytest.mark.parametrize(
        "url, ok",
        [
            ("https://github.com/user-cont/kwaciaren", True),
            ("https://github.com/somedummy/somereallydummy", False),
        ],
    )
    def test_call_git_cmd_clone(self, tmpdir, url, ok):
        """Test Git.clone()."""
        tmpdir = str(tmpdir)
        if ok:
            assert Git.call_git_cmd(f"clone --depth=1 --single-branch {url} {tmpdir}")
            assert isdir(join(tmpdir, ".git"))
            assert isfile(join(tmpdir, "README.md"))
        else:
            with pytest.raises(CalledProcessError):
                Git.call_git_cmd(f"clone {url} {tmpdir}")

    @pytest.mark.parametrize(
        "url",
        [
            "github.com/foo/bar",
            "github.com/foo/bar.git",
            "www.github.com/foo/bar",
            "http://github.com/foo/bar",
            "http://github.com/foo/bar.git",
            "git+https://www.github.com/foo/bar",
            "git@github.com:foo/bar",
            "git@github.com:foo/bar.git",
            "git+ssh@github.com:foo/bar.git",
            "ssh://git@github.com:foo/bar.git",
            "gitlab.domain.com/foo/bar",
            "git@gitlab.domain.com:foo/bar.git",
            "https://bitbucket.org/foo/bar",
            "ssh://git@git.src.domain.com:32101/foo/bar.git",
        ],
    )
    def test_parse_gh_repo_ok(self, url):
        """Test parse_gh_repo()."""
        assert Git.parse_git_repo(url) == ("foo", "bar")
        assert Git.get_username_from_git_url(url) == "foo"
        assert Git.get_reponame_from_git_url(url) == "bar"

    @pytest.mark.parametrize(
        "url", ["something", "something@else", "http://github.com/user/repo/something"]
    )
    def test_parse_gh_repo_nok(self, url):
        """Test parse_gh_repo()."""
        assert Git.parse_git_repo(url) is None

    @pytest.mark.parametrize(
        "url, expected_result",
        [
            ("git@gitlab.domain.com:foo/bar.git", "git@gitlab.domain.com:foo/bar"),
            ("github.com/foo/bar", "github.com/foo/bar"),
        ],
    )
    def test_strip_dot_git(self, url, expected_result):
        """Test strip_dot_git()."""
        assert Git.strip_dot_git(url) == expected_result

    def test_create_dot_gitconfig(self, tmpdir):
        Git.call_git_cmd(f"init {tmpdir}")
        user_name = "Jara Cimrman"
        Git.create_dot_gitconfig(user_name=user_name, user_email="mail")
        assert Git.call_git_cmd(f"config --get user.name").strip() == user_name
