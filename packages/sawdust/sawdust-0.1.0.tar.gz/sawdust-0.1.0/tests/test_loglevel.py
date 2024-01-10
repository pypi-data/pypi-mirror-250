import logging

from sawdust import LogLevel


def test_as_logging_module_level():
    assert LogLevel.DEBUG.as_logging_module_level == logging.DEBUG
    assert LogLevel.INFO.as_logging_module_level == logging.INFO
    assert LogLevel.WARNING.as_logging_module_level == logging.WARNING
    assert LogLevel.ERROR.as_logging_module_level == logging.ERROR
    assert LogLevel.CRITICAL.as_logging_module_level == logging.CRITICAL
