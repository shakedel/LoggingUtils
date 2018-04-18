import logging

import os

import pytest

# the 'logger' fixture is used implicitly in testing method signatures. must
# be manually imported
# noinspection PyUnresolvedReferences
from test.testingutils import logger

from test.testingutils import LoggerHandlers
from loggingutils.handlers import MakedirsFileHandler


def test_sanityCheck(logger, tmpdir):
    """
    A basic test to see that standard logging succeeds. Also shows how to use
    the 'logger' fixture and 'LoggerHandlers' context manager.
    """
    logpath = os.path.join(tmpdir, __name__ + '_sanity.log')
    with LoggerHandlers(logger, logging.FileHandler(logpath)):
        logger.info('some info msg')
    assert True


def test_makeDirsFileHander(logger, tmpdir):
    """
    Tests that log paths with missing directories fails with vanilla
    FileHandler but succeeds with MakedirsFileHandler
    """
    logpath = os.path.join(tmpdir, 'nonexistingdir', __name__
                           + '_mkdirsfilehandler.log')

    # this should fail as we are using a standard logger with a non-existing
    # dirs in its path
    with pytest.raises(FileNotFoundError, message='expected to fail over '
                                                  'missing directory'):
        with LoggerHandlers(logger, logging.FileHandler(logpath)):
            logger.info('some info msg')

    # the custom hander should succeed with missing dirs
    handler = MakedirsFileHandler(logpath)
    with LoggerHandlers(logger, handler):
        logger.info('some info msg')
        newdir = os.path.dirname(logpath)
        assert os.path.isdir(newdir)
