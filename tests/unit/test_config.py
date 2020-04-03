import json
from pathlib import Path

import pytest

from frambo import config


class TestConfig:
    def test_dict_merge(self):
        dct = {"a": 1, "b": {"b1": 2, "b2": 3}}
        merge_dct = {"a": 1, "b": {"b1": 4}}

        config.dict_merge(dct, merge_dct)
        assert dct["a"] == 1
        assert dct["b"]["b1"] == 4
        assert dct["b"]["b2"] == 3

        merge_dct = {"a": 1, "b": {"b1": 4, "b3": 5}, "c": 6}

        config.dict_merge(dct, merge_dct)
        assert dct["a"] == 1
        assert dct["b"]["b1"] == 4
        assert dct["b"]["b2"] == 3
        assert dct["b"]["b3"] == 5
        assert dct["c"] == 6

    @pytest.mark.parametrize(
        "bot_cfg_path",
        [
            Path(__file__).parent.parent / "data/bot-configs/bot-cfg.yml",
            Path(__file__).parent.parent / "data/bot-configs/bot-cfg-default.yml",
            Path(__file__).parent.parent / "data/bot-configs/bot-cfg-old-keys.yml",
        ],
    )
    def test_load_configuration(self, bot_cfg_path):
        from_file = config.load_configuration(conf_path=bot_cfg_path)
        from_string = config.load_configuration(conf_str=bot_cfg_path.read_text())
        assert from_file == from_string

        # no arguments -> default config
        assert config.load_configuration()

        with pytest.raises(AttributeError):
            config.load_configuration("both args", "specified")

        with pytest.raises(AttributeError):
            config.load_configuration(conf_path="/does/not/exist")

    def test_load_configuration_with_aliases(self):
        my = {
            "version": "2",
            "zdravomil": {"enabled": False},
            "betka": {"enabled": False},
        }
        conf = config.load_configuration(conf_str=json.dumps(my))
        # our 'zdravomil' key has been merged into default's 'dockerfile-linter' key
        assert conf["dockerfile-linter"]["enabled"] is False
        assert conf["upstream-to-downstream"]["enabled"] is False

    @pytest.mark.parametrize(
        "cfg_url",
        ["https://github.com/user-cont/frambo/raw/master/examples/cfg/bot-cfg.yml"],
    )
    def test_fetch_config(self, cfg_url):
        c1 = config.fetch_config("zdravomil", cfg_url)
        c2 = config.fetch_config("dockerfile-linter", cfg_url)
        c3 = config.fetch_config("betka", cfg_url)
        c4 = config.fetch_config("upstream-to-downstream", cfg_url)
        assert c1 == c2
        # make sure the 'global' key has been merged into all bots` keys
        assert "notifications" in c1
        assert c3 == c4
        assert "notifications" in c3

    def test_get_from_frambo_config(self):
        assert config.get_from_frambo_config("emails", "sender")
        assert config.get_from_frambo_config("pagure", "host")

    def test_frambo_config_ok(self):
        path = Path(__file__).parent.parent / "data/configs/ok-config"
        conf = config.frambo_config(path)
        assert conf["emails"]["smtp_server"] == "elm.street"
        assert conf["pagure"]["host"] == "test"

    @pytest.mark.parametrize(
        "data_path", ["no-config/", "empty-config/", "list-but-no-deployment/"]
    )
    def test_frambo_config_not_ok(self, data_path):
        path = Path(__file__).parent.parent / "data/configs/" / data_path
        with pytest.raises(Exception):
            config.frambo_config(path)
