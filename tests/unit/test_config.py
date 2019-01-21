import json
from pathlib import Path

import pytest

from frambo import config


class TestConfig:

    @pytest.fixture
    def config_path(self):
        return Path(__file__).parent.parent / "data/bot-cfg.yml"

    def test_dict_merge(self):
        dct = {
            'a': 1,
            'b': {
                'b1': 2,
                'b2': 3,
            },
        }
        merge_dct = {
            'a': 1,
            'b': {
                'b1': 4,
            },
        }

        config.dict_merge(dct, merge_dct)
        assert dct['a'] == 1
        assert dct['b']['b1'] == 4
        assert dct['b']['b2'] == 3

        merge_dct = {
            'a': 1,
            'b': {
                'b1': 4,
                'b3': 5
            },
            'c': 6,
        }

        config.dict_merge(dct, merge_dct)
        assert dct['a'] == 1
        assert dct['b']['b1'] == 4
        assert dct['b']['b2'] == 3
        assert dct['b']['b3'] == 5
        assert dct['c'] == 6

    def test_load_configuration(self, config_path):
        from_file = config.load_configuration(conf_path=config_path)
        from_string = config.load_configuration(conf_str=config_path.read_text())
        assert from_file == from_string

        # no arguments -> default config
        assert config.load_configuration()

        with pytest.raises(AttributeError):
            config.load_configuration('both args', 'specified')

        with pytest.raises(AttributeError):
            config.load_configuration(conf_path='/does/not/exist')

    def test_load_configuration_with_aliases(self):
        my = {
            "version": "2",
            "zdravomil": {
                "enabled": False
            },
            "upstream-to-downstream": {
                "enabled": True,
                "master_checker": True
            }
        }
        conf = config.load_configuration(conf_str=json.dumps(my))
        # our 'zdravomil' key has been merged into default's 'dockerfile-linter' key
        assert conf['dockerfile-linter']['enabled'] is False
        assert conf['upstream-to-downstream']['enabled'] is True
