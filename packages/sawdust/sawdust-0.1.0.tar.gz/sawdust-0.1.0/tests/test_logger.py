import logging
import os

from sawdust import Logger, LogLevel, LogFormat
from tests.utils import delete_file


def test__add_handler():
    logger = Logger(name='test__add_handler', level=LogLevel.INFO)
    handler = logging.StreamHandler()

    logger._add_handler(handler=handler, level=LogLevel.DEBUG, msg_format=LogFormat())

    assert len(logger._logger.handlers) == 1

    # Can't add the same handler twice
    logger._add_handler(handler=handler, level=LogLevel.FATAL, msg_format=LogFormat())

    assert len(logger._logger.handlers) == 1

    # Can add two of the same type of handler, though
    handler2 = logging.StreamHandler()

    logger._add_handler(handler=handler2, level=LogLevel.FATAL, msg_format=LogFormat())

    assert len(logger._logger.handlers) == 2


def test_log_to_console():
    logger = Logger(name='test_log_to_console', level=LogLevel.INFO)
    logger.log_to_console(level=LogLevel.DEBUG)

    assert len(logger._logger.handlers) == 1
    assert logger._logger.handlers[0].formatter._fmt == '%(message)s'
    assert logger._logger.handlers[0].level == LogLevel.DEBUG.as_logging_module_level

    logger.debug(message='test_log_to_console')


def test_log_to_file():
    logger = Logger(name='test_log_to_file', level=LogLevel.INFO)
    logger.log_to_file(folder_path="unit/logs", level=LogLevel.DEBUG)

    assert len(logger._logger.handlers) == 1
    assert logger._logger.handlers[0].formatter._fmt == '%(asctime)s - [%(levelname)s]: %(message)s'
    assert logger._logger.handlers[0].level == LogLevel.DEBUG.as_logging_module_level

    logger.debug(message='test_log_to_file')


def test_fatal():
    log_file_folder = 'unit/logs'
    log_file_name = 'test_fatal.log'

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = Logger(name='test_fatal', level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=LogLevel.FATAL)

    logger.fatal(message='test_fatal')

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert '[CRITICAL]: test_fatal' in log_file_contents


def test_critical():
    log_file_folder = 'unit/logs'
    log_file_name = 'test_critical.log'
    message = 'test_critical'
    level = LogLevel.CRITICAL
    level_str = "[CRITICAL]"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = Logger(name=message, level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=level)

    logger.critical(message=message)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert f'{level_str}: {message}' in log_file_contents


def test_error():
    log_file_folder = 'unit/logs'
    log_file_name = 'test_error.log'
    message = 'test_error'
    level = LogLevel.ERROR
    level_str = "[ERROR]"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = Logger(name=message, level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=level)

    logger.error(message=message)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert f'{level_str}: {message}' in log_file_contents


def test_warning():
    log_file_folder = 'unit/logs'
    log_file_name = 'test_warning.log'
    message = 'test_warning'
    level = LogLevel.WARNING
    level_str = "[WARNING]"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = Logger(name=message, level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=level)

    logger.warning(message=message)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert f'{level_str}: {message}' in log_file_contents


def test_warn():
    log_file_folder = 'unit/logs'
    log_file_name = 'test_warn.log'
    message = 'test_warn'
    level = LogLevel.WARNING
    level_str = "[WARNING]"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = Logger(name=message, level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=level)

    logger.warn(message=message)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert f'{level_str}: {message}' in log_file_contents


def test_info():
    log_file_folder = 'unit/logs'
    log_file_name = 'test_info.log'
    message = 'test_info'
    level = LogLevel.INFO
    level_str = "[INFO]"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = Logger(name=message, level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=level)

    logger.info(message=message)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert f'{level_str}: {message}' in log_file_contents


def test_debug():
    log_file_folder = 'unit/logs'
    log_file_name = 'test_debug.log'
    message = 'test_debug'
    level = LogLevel.DEBUG
    level_str = "[DEBUG]"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = Logger(name=message, level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=level)

    logger.debug(message=message)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert f'{level_str}: {message}' in log_file_contents
