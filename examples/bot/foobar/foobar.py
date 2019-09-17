from os import listdir
from tempfile import TemporaryDirectory, mkstemp

from frambo.bot import Bot
from frambo.utils import run_cmd


class FooBarBot(Bot):
    """
    Your bot implementation.
    Here you can extend/override Bot.
    """

    def __init__(self, task_name=None):
        super().__init__(task_name=task_name)
        self.tmpdir = TemporaryDirectory()
        self.tmpfile = None

    def process(self, msg):
        """All task's work is done here."""
        self.debug("processing")
        run_cmd(["sleep", "1"])  # Hardly working on it
        # make sure there are no files from previous run
        assert not listdir(self.tmpdir.name)
        _, self.tmpfile = mkstemp(dir=self.tmpdir.name)
        self.error("error message example")
        return f"Hello, I'm FooBarBot. {msg}"

    def log(self, level, msg, *args, **kwargs):
        """
        Overrides Bot.log() to log specific attributes of this bot.
        If you are overriding log() for your bot, create
        report_dict = {
            'message': self.logger.format(msg, args)
        }
        and add more attributes, which you want to be included in each logged message.

        :param level: logging level as defined in logging module
        :param msg: message to log
        :param args: arguments to msg
        """
        report_dict = {
            "message": self.logger.format(msg, args),
            "tmpdir": self.tmpdir.name,
            "tmpfile": self.tmpfile,
        }
        self.logger.log(level, report_dict)
