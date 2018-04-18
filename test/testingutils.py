import logging

from _pytest.fixtures import fixture


class LoggerHandlers:
    """
    A context manager to add handlers to a logger and remove them after
    execution.
    The logger provided is returned for convenience
    """
    def __init__(self, logger, *args):
        self.logger = logger
        self.handlers = args

    def __enter__(self):
        [self.logger.addHandler(handler) for handler in self.handlers]
        return self.logger

    def __exit__(self, *args):
        [self.logger.removeHandler(handler) for handler in self.handlers]


@fixture
def logger(request):
    """
    A pytest fixture to create custom loggers per testing method
    """
    return logging.getLogger(__name__+'__'+request.function.__name__)