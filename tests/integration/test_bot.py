"""Test Bot class"""

from flexmock import flexmock
from pathlib import Path
import pytest

from frambo.bot import Bot


class TestBot:
    """Test Bot class"""

    @pytest.fixture
    def config_path(self):
        return Path(__file__).parent.parent / "data/bot-cfg.yml"

    @pytest.fixture()
    def bot(self):
        return Bot()

    @pytest.mark.parametrize("key, result", [
        ("dockerfile-linter", True),
    ])
    def test_is_enabled(self, bot, config_path, key, result):
        flexmock(bot, cfg_key=key)
        assert bot.is_enabled(config_path=config_path) == result
