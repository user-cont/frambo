# -*- coding: utf-8 -*-

"""Test Logger class."""

import logging
import pytest

from frambo.logger import Logger

logger = logging.getLogger(__name__)


class TestLogger(object):
    """Test Logger class."""

    @pytest.mark.parametrize(
        "msg, args, fmsg",
        [
            ("hello %s", ("beautiful",), "hello beautiful"),
            (u"čau", tuple(), u"čau"),
            (b"\xc4\x8dau", tuple(), u"čau"),
            (123, None, 123),
        ],
    )
    def test_format(self, msg, args, fmsg):
        assert Logger.format(msg, args) == fmsg
