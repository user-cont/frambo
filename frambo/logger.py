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

from celery.utils.log import get_task_logger
from datetime import datetime
import json
import logging
import os


class Logger(object):
    """
    Log by
     - logging to stderr (default)
     - writing json to file
    """

    def __init__(
        self,
        task_name,
        level=logging.NOTSET,
        to_file=True,
        file_path=None,
        additional=None,
    ):
        """
        Initialize.

        :param task_name: Celery task name
        :param level:  logger level
        :param to_file: log to file ?
        :param file_path: which file to log to, defaults to /var/log/bots/{task}.log-{date}
        :param additional: additional string to include in log file name
        """
        self.task_name = task_name
        self.logger = (
            get_task_logger(task_name) if task_name else logging.getLogger(__name__)
        )
        self.logger.setLevel(level)
        self.log_file = None

        if not task_name:
            # add stderr handler only if there's no task_name since Celery workers already have one
            self.logger.addHandler(logging.StreamHandler())

        if to_file:
            if file_path:
                if additional:
                    raise ValueError("file_path and additional can't be both defined")
                if not os.path.isdir(os.path.dirname(file_path)):
                    self.logger.error(
                        "{} is not a directory".format(os.path.dirname(file_path))
                    )
                    return
            else:  # file_path not specified, will log to default location
                try:
                    file_path = self.file_path(additional=additional)
                except RuntimeError as exc:
                    # default log dir doesn't exist
                    self.logger.error(exc)
                    return
            self.log_file = file_path
            file_handler = logging.FileHandler(file_path)
            self.logger.addHandler(file_handler)

    def file_path(self, additional=None, date=True):
        """
        Return path to file where logs will be saved.

        :param additional: additional string to include in log file name
        :param date: include date (YMD) in log file name
        :returns if both additional and date then /var/log/bots/{task}-{additional}.log-{date}
        """
        logs_dir = os.getenv("LOGS_DIR") or "/var/log/bots"
        if not os.path.isdir(logs_dir):
            raise RuntimeError("{} is not a directory".format(logs_dir))

        return (
            "{dir}/{task}{additional}.log{date}".format(
                dir=logs_dir,
                task=self.task_name,
                additional="-" + additional if additional else "",
                date="-" + datetime.now().strftime("%Y%m%d"),
            )
            if date
            else ""
        )

    @staticmethod
    def format(msg, args):
        """

        :param msg: message to log
        :param args: arguments to msg
        """
        if isinstance(msg, bytes):
            msg = msg.decode("utf-8")
        return msg % args if args else msg

    def log(self, level, report_dict):
        """
        Logging workhorse.

        :param level: logging level as defined in logging module
        :param report_dict: dictionary to be logged, mandatory keys: 'message'
        """
        msg = self.serialize(level, report_dict)
        if level == logging.CRITICAL:
            self.logger.critical(msg)
        elif level == logging.ERROR:
            self.logger.error(msg)
        elif level == logging.WARNING:
            self.logger.warning(msg)
        elif level == logging.INFO:
            self.logger.info(msg)
        elif level == logging.DEBUG:
            self.logger.debug(msg)

    def serialize(self, level, report_dict):
        """
        Fill in additional info to report_dict and serialize it.

        :param level: logging level as defined in logging module
        :param report_dict: dictionary to be logged
        :return:
        """
        report_dict.update(
            {
                "level": logging.getLevelName(level),
                "task": self.task_name,
                "time": str(datetime.utcnow()),
            }
        )
        serialized = json.dumps(report_dict, sort_keys=True, indent=2)
        # HACK: Pretty print newlines in values - strings. Feel free to fix it if you know better.
        serialized = serialized.replace("\\n", "\n")
        return serialized
