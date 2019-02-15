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

from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG

from frambo.config import fetch_config, load_configuration
from frambo.logger import Logger


class Bot:
    """Attributes/methods common to all bot-tasks.
       Center piece of the bot framework where most of the logic for bots will live.
    """

    # To be set in subclasses
    cfg_key = None

    def __init__(self, logger=None, task_name=None):
        """
        Initialize.

        :param logger: if a Bot (subclass) instance wants to use differently configured Logger
        :param task_name: str, for logging purposes, name of task which created this Bot instance
        """
        self.logger = logger or Logger(task_name=task_name, level=DEBUG)
        self.config = None

    def is_enabled(self, config_url=None, config_path=None):
        """
        Is bot enabled in config ?
        If config_url OR config_path is provided, fetch/load the config first
        """
        if config_url and config_path:
            raise AttributeError("Provide EITHER config_url OR config_path")

        if config_url:
            self.config = fetch_config(self.cfg_key, config_url)
        elif config_path:
            self.config = load_configuration(config_path).get(self.cfg_key, {})

        if not self.config:
            raise RuntimeError("config has not been loaded yet")

        return self.config.get("enabled", False)

    def log(self, level, msg, *args, **kwargs):
        """
        Log to stderr/file.

        This method should be overridden in a subclass
        in order to log subclass's specific attributes.

        If you are overriding log() for your bot,
        copy content of this method and add more attributes into report_dict.
        These attributes will be included in each logged message.
        See example/foobar/foobar.py.

        :param level: logging level as defined in logging module
        :param msg: message to log
        :param args: arguments to msg
        """
        report_dict = {
            'message': self.logger.format(msg, args)
        }
        self.logger.log(level, report_dict)

    def critical(self, msg, *args, **kwargs):
        self.log(CRITICAL, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log(ERROR, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log(WARNING, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log(INFO, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.log(DEBUG, msg, *args, **kwargs)

    def exception(self, exception):
        self.logger.logger.exception(exception)
