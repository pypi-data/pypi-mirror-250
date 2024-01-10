import os

import sawdust
from sawdust import LogLevel
from tests.utils import delete_file


def test__is_lower_log_level():
    assert sawdust.logging._is_lower_log_level(
        level=LogLevel.DEBUG.as_logging_module_level, other_level=LogLevel.INFO.as_logging_module_level) is True

    assert sawdust.logging._is_lower_log_level(
        level=LogLevel.INFO.as_logging_module_level, other_level=LogLevel.DEBUG.as_logging_module_level) is False

    assert sawdust.logging._is_lower_log_level(
        level=LogLevel.INFO.as_logging_module_level, other_level=LogLevel.INFO.as_logging_module_level) is False

    assert sawdust.logging._is_lower_log_level(
        level=LogLevel.DEBUG.as_logging_module_level, other_level=LogLevel.DEBUG.as_logging_module_level) is False


def test__get_logging_logger():
    logger = sawdust.logging._get_logging_logger(name='test__get_logging_logger')

    assert logger.name == 'test__get_logging_logger'


def test__get():
    # Get a logger that doesn't exist (create it)
    logger = sawdust.logging._get(name='test_get')
    # Since new, level should be the default
    assert logger._logger.level == sawdust.logging.DEFAULT_LOG_LEVEL.as_logging_module_level

    # Set the level to something else
    logger._logger.setLevel(sawdust.logging.LogLevel.DEBUG.as_logging_module_level)

    # Get the logger again (shouldn't create a new one, but return the existing one from cache)
    logger = sawdust.logging._get(name='test_get')
    # Since it already exists, level should be whatever was set
    assert logger._logger.level == sawdust.logging.LogLevel.DEBUG.as_logging_module_level


def test_fatal():
    log_file_folder = 'unit/logs'
    logger_name = 'test_fatal'
    log_file_name = f"{logger_name}.log"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = sawdust.Logger(name='test_fatal', level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=LogLevel.FATAL)

    sawdust.fatal(message='test_fatal', specific_logger=logger_name)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert '[CRITICAL]: test_fatal' in log_file_contents


def test_critical():
    log_file_folder = 'unit/logs'
    logger_name = 'test_critical'
    log_file_name = f"{logger_name}.log"
    message = 'test_critical'
    level = LogLevel.CRITICAL
    level_str = "[CRITICAL]"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = sawdust.Logger(name=message, level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=level)

    sawdust.critical(message=message, specific_logger=logger_name)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert f'{level_str}: {message}' in log_file_contents


def test_error():
    log_file_folder = 'unit/logs'
    logger_name = 'test_error'
    log_file_name = f"{logger_name}.log"
    message = 'test_error'
    level = LogLevel.ERROR
    level_str = "[ERROR]"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = sawdust.Logger(name=message, level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=level)

    sawdust.error(message=message, specific_logger=logger_name)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert f'{level_str}: {message}' in log_file_contents


def test_warning():
    log_file_folder = 'unit/logs'
    logger_name = 'test_warning'
    log_file_name = f"{logger_name}.log"
    message = 'test_warning'
    level = LogLevel.WARNING
    level_str = "[WARNING]"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = sawdust.Logger(name=message, level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=level)

    sawdust.warning(message=message, specific_logger=logger_name)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert f'{level_str}: {message}' in log_file_contents


def test_warn():
    log_file_folder = 'unit/logs'
    logger_name = 'test_warn'
    log_file_name = f"{logger_name}.log"
    message = 'test_warn'
    level = LogLevel.WARNING
    level_str = "[WARNING]"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = sawdust.Logger(name=message, level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=level)

    sawdust.warn(message=message, specific_logger=logger_name)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert f'{level_str}: {message}' in log_file_contents


def test_info():
    log_file_folder = 'unit/logs'
    logger_name = 'test_info'
    log_file_name = f"{logger_name}.log"
    message = 'test_info'
    level = LogLevel.INFO
    level_str = "[INFO]"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = sawdust.Logger(name=message, level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=level)

    sawdust.info(message=message, specific_logger=logger_name)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert f'{level_str}: {message}' in log_file_contents


def test_debug():
    log_file_folder = 'unit/logs'
    logger_name = 'test_debug'
    log_file_name = f"{logger_name}.log"
    message = 'test_debug'
    level = LogLevel.DEBUG
    level_str = "[DEBUG]"

    delete_file(folder_path=log_file_folder, file_name=log_file_name)

    logger = sawdust.Logger(name=message, level=LogLevel.INFO)
    logger.log_to_file(folder_path=log_file_folder, file_name=log_file_name, level=level)

    sawdust.debug(message=message, specific_logger=logger_name)

    with open(os.path.join(log_file_folder, log_file_name), 'r') as log_file:
        log_file_contents = log_file.read()
        assert f'{level_str}: {message}' in log_file_contents
