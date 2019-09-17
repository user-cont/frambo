"""Test utilities from utils.py"""

import pytest
from subprocess import CalledProcessError

from frambo.utils import run_cmd


class TestUtils(object):
    """Test utilities from utils.py"""

    @pytest.mark.parametrize(
        "cmd, ok", [(["ls", "-la"], True), (["ls", "--nonexisting"], False)]
    )
    def test_run_cmd(self, cmd, ok):
        """Test run_cmd()."""
        if ok:
            assert run_cmd(cmd, return_output=True).startswith("total ")
            assert run_cmd(cmd, return_output=False) == 0
        else:
            with pytest.raises(CalledProcessError):
                run_cmd(cmd, ignore_error=False)
            assert run_cmd(cmd, ignore_error=True, return_output=True)
            assert run_cmd(cmd, ignore_error=True, return_output=False) > 0
