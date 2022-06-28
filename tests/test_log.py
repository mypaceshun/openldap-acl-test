from logging import Logger

from openldap_acl_test import __name__
from openldap_acl_test.log import init_logger


def test_logger():
    logger = init_logger(__name__)
    assert isinstance(logger, Logger)


def test_logger_stdout_stderr(capsys):
    logger = init_logger(__name__)
    logger.info("info message")
    logger.error("error message")
    captured = capsys.readouterr()
    assert captured.out == "info message\n"
    assert captured.err == "error message\n"
