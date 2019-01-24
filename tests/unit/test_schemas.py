from pathlib import Path

import jsonschema
import pytest
from yaml import safe_load

from frambo.schemas import BotCfg


class TestSchemas:
    """
    Test schemas.py
    """

    @pytest.fixture
    def example_bot_cfg(self):
        path = Path(__file__).parent.parent / "data/bot-configs/bot-cfg.yml"
        return safe_load(open(path))

    @pytest.fixture
    def bad_cfg(self):
        path = Path(__file__).parent.parent / "data/bot-configs/bad-cfg.yml"
        return safe_load(open(path))

    def test_example_bot_cfg(self, example_bot_cfg):
        jsonschema.validate(example_bot_cfg, BotCfg.get_schema())

    def test_bad_bot_cfg(self, bad_cfg):
        with pytest.raises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(bad_cfg, BotCfg.get_schema())
