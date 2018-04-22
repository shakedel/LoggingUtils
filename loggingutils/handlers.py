

"""
A log handler that rotates when either a time or size limit is reached
"""
from logging import FileHandler
from time import time, localtime
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import os


# pylint: disable=too-many-ancestors
class TimeOrSizeRotatingFileHandler(TimedRotatingFileHandler,
                                    RotatingFileHandler):
    """
    A log handler that rotates when either a time or size limit is reached
    """
    # pylint: disable=too-many-arguments
    def __init__(self,
                 filename: str,
                 mode: str = 'a',
                 maxBytes: int = 0,
                 backupCount: int = 0,
                 encoding=None,
                 delay: int = 0,
                 when: str = 'H',
                 interval: int = 1,
                 utc: bool = False):
        TimedRotatingFileHandler.__init__(
            self,
            filename=filename, when=when, interval=interval,
            backupCount=backupCount, encoding=encoding, delay=delay, utc=utc)

        RotatingFileHandler.__init__(self, filename=filename, mode=mode, maxBytes=maxBytes,
                                     backupCount=backupCount, encoding=encoding, delay=delay)

    def computeRollover(self, currentTime) -> int:
        return TimedRotatingFileHandler.computeRollover(self, currentTime)

    def doRollover(self):
        # get from logging.handlers.TimedRotatingFileHandler.doRollover()
        current_time = int(time())
        dst_now = localtime(current_time)[-1]
        new_rollover_at = self.computeRollover(current_time)

        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval

        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dst_at_rollover = localtime(new_rollover_at)[-1]
            if dst_now != dst_at_rollover:
                if not dst_now:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                new_rollover_at += addend
        self.rolloverAt = new_rollover_at
        TimedRotatingFileHandler.doRollover(self)

    def shouldRollover(self, record) -> bool:
        timed = TimedRotatingFileHandler.shouldRollover(self, record)
        size = RotatingFileHandler.shouldRollover(self, record)
        return timed or size


class MakedirsFileHandler(FileHandler):
    """
    A log handler that creates all missing dirs in its path
    https://stackoverflow.com/a/20667049/2261244 (unutbu)

    """

    def __init__(self,
                 filename: str,
                 mode: str ='a',
                 encoding=None,
                 delay: bool = 0):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        FileHandler.__init__(self, filename, mode, encoding, delay)
