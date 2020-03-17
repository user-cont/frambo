#!/usr/bin/env python3

import copy
from functools import lru_cache
import json
import jsonschema
import logging
from os import getenv
from pathlib import Path
import requests
import sys
import yaml

from typing import Any

from frambo.schemas import BotCfg

BASE_PATH = Path(__file__).parent
DATA_PATH = BASE_PATH / "data"
CONFIG_DIR = DATA_PATH / "conf.d"
DEFAULTS_PATH = DATA_PATH / "defaults/conf-defaults-v1.yml"

DEPLOYMENT = getenv("DEPLOYMENT")
if not DEPLOYMENT:
    raise ValueError("Please set DEPLOYMENT environment variable.")

logger = logging.getLogger(__name__)


@lru_cache(maxsize=4)
def frambo_config(cfgdir=CONFIG_DIR):
    """
    Load & return frambo configuration from cfgdir.
    :param cfgdir: pathlike
    """
    cfgfile = cfgdir / "config.yml"
    logger.info(f"Loading frambo config: {cfgfile}")
    config = yaml.safe_load(open(cfgfile))
    if not config:
        raise ValueError("No frambo config found")

    for module, values in config.items():
        # if it's list of entries, select the one whose 'deployment' == DEPLOYMENT
        if isinstance(values, list):
            for entry in values:
                if "deployment" not in entry:
                    raise ValueError(f"No 'deployment' in {entry}")
                if not isinstance(entry["deployment"], list):
                    entry["deployment"] = [entry["deployment"]]
                if DEPLOYMENT in entry["deployment"]:
                    entry.pop("deployment")
                    config[module] = entry
                    break
    return config


def get_from_frambo_config(
    module: str,
    key: str,
    default: Any = "",
    raises: bool = True,
) -> str:

    if key not in frambo_config().get(module, {}) and raises:
        raise ValueError(f"{module}:{key} not set in {CONFIG_DIR / 'config.yml'}")
    return frambo_config().get(module, {}).get(key, default)


BOT_CONF_KEYS_ALIASES = get_from_frambo_config("config", "bot-conf-keys-aliases")
BOT_CONF_KEYS = set(BOT_CONF_KEYS_ALIASES.values())


def alias2key(alias):
    return BOT_CONF_KEYS_ALIASES.get(alias, alias)


def dict_merge(into_dct, from_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``from_dct`` is merged into
    ``into_dct``.
    :param into_dct: dict, onto which the merge is executed
    :param from_dct: dict, merged into into_dct
    :return: None
    """
    for k, v in from_dct.items():
        k = alias2key(k)
        if isinstance(into_dct.get(k), dict) and isinstance(v, dict):
            dict_merge(into_dct[k], v)
        else:
            into_dct[k] = copy.deepcopy(v) if isinstance(v, dict) else v


def pretty_dict(report_dict):
    result = json.dumps(report_dict, sort_keys=True, indent=4)
    result = result.replace("\\n", "\n")
    return result


def fetch_config(config_key, config_file_url):
    if not config_key:
        raise AttributeError(
            "No configuration key."
            "You probably need to set bot_cfg attribute in your bot."
        )
    if alias2key(config_key) not in BOT_CONF_KEYS:
        raise AttributeError(
            f"Unknown bot configuration key {config_key!r}."
            f"Supported are: {BOT_CONF_KEYS}."
        )

    bots_config = ""
    logger.info(f"Pulling config file: {config_file_url}")
    r = requests.get(config_file_url, cookies={"pagure": "user-cont-bot-cfg-load"})
    if r.status_code == 200:
        bots_config = r.text
        logger.debug("Bot configuration fetched")
    else:
        logger.warning(
            f"Config file not found in url: {config_file_url}, "
            "using default configuration."
        )

    conf_with_defaults = load_configuration(conf_str=bots_config)
    return conf_with_defaults[alias2key(config_key)]


def load_configuration(conf_path=None, conf_str=None):
    # load defaults
    result = yaml.safe_load(open(DEFAULTS_PATH))
    # logger.debug(f"Default bots configuration: {pretty_dict(result)}")

    if conf_str and conf_path:
        raise AttributeError(
            "Provided both forms of configuration."
            "Use only conf_path or only conf_str"
        )

    if not (conf_str or conf_path):
        # none provided, return default config
        logger.info("No config provided, using default")
        return result

    if conf_path:
        if not Path(conf_path).is_file():
            raise AttributeError(f"Configuration file not found: {conf_path}")
        conf_str = Path(conf_path).read_text()

    # Some people keep putting tabs at the end of lines
    conf_str = conf_str.replace("\t\n", "\n")

    repo_conf = yaml.safe_load(conf_str)

    for bot_key in repo_conf.keys():
        if alias2key(bot_key) not in BOT_CONF_KEYS.union({"version", "global"}):
            logger.warning(
                f"Provided unsupported key value: {bot_key}. "
                f"Supported are: {BOT_CONF_KEYS}."
            )

    # fill global values
    for key in BOT_CONF_KEYS:
        try:
            dict_merge(
                into_dct=result.get(key, {}), from_dct=repo_conf.get("global", {})
            )
        except AttributeError:
            # 'global' key has probably just some non-dict value like None or '', no need to raise
            logger.error(f"Wrong 'global' value: {repo_conf['global']}")
    # 'global' has been merged into others, we don't need it anymore
    repo_conf.pop("global", None)

    # overwrite defaults with values in bot configuration
    dict_merge(into_dct=result, from_dct=repo_conf)

    # validate
    jsonschema.validate(result, BotCfg.get_schema())

    logger.debug(f"Resulting bots configuration: {pretty_dict(result)}")

    return result


if __name__ == "__main__":
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    if len(sys.argv) > 1:
        conf = load_configuration(sys.argv[1])
    else:
        conf = load_configuration()
