import enum
import logging
import logging.handlers
import os
from typing import (Optional)


class LogFormat:
    _time_format = ''
    _level_format = ''
    _function_format = ''
    _name_format = ''
    _process_format = ''

    def __init__(self, mgs_format: str = None):
        self._format = mgs_format

    def include_time(self) -> 'LogFormat':
        self._time_format = '%(asctime)s'
        return self

    def include_level(self, in_brackets: bool = False) -> 'LogFormat':
        self._level_format = '%(levelname)s'
        if in_brackets:
            self._level_format = f'[{self._level_format}]'
        return self

    def include_calling_function(self) -> 'LogFormat':
        self._function_format = '%(module)s.%(funcName)s'
        return self

    def include_process_name(self) -> 'LogFormat':
        self._process_format = '%(processName)s'
        return self

    def include_logger_name(self) -> 'LogFormat':
        self._name_format = '%(name)s'
        return self

    def build(self) -> str:
        # If the user provided a format, we'll just use that
        if self._format:
            return self._format

        # Build the prefix with the enabled elements
        # LOGGER_NAME - TIMESTAMP - LOG_LEVEL - PROCESS - FUNCTION
        _elements = [
            elem for elem in [
                self._name_format,
                self._time_format,
                self._level_format,
                self._process_format,
                self._function_format,
            ] if elem != ''
        ]
        _prefix = f'{" - ".join(_elements)}:' if _elements else ''

        return f'{_prefix} %(message)s'.strip()


class LogLevel(enum.Enum):
    CRITICAL = logging.CRITICAL
    FATAL = CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET

    @property
    def as_logging_module_level(self) -> int:
        return self.value


# 200kb * 5 files = 1mb of logs
DEFAULT_LOG_MAX_BYTES = 200000  # 200kb
DEFAULT_LOG_BACKUP_COUNT = 5

DEFAULT_LOG_LEVEL = LogLevel.INFO

# %(message)s
DEFAULT_CONSOLE_FORMAT = LogFormat()
# %(asctime)s - [%(levelname)s]: %(message)s
DEFAULT_FILE_FORMAT = LogFormat().include_time().include_level(in_brackets=True)

DEFAULT_LOGGER_NAME = 'sawdust'


def _is_lower_log_level(level: int, other_level: int) -> bool:
    """Internal utility to check if a log level is lower than another."""
    return level < other_level


def _get_logging_logger(name: str) -> logging.Logger:
    """Internal utility to get or create a logger instance by name."""
    logger = logging.getLogger(name)  # Will retrieve an existing logger or create a new one

    return logger


class Logger:
    def __init__(self, name: str = DEFAULT_LOGGER_NAME, level: LogLevel = DEFAULT_LOG_LEVEL):
        """
        Set up a logger based on a provided set of input.

        :param name: The name of the logger, typically the name of the module using logging
        :type name: str
        :param level: The log level of the logger.
        :type level: Union[CRITICAL, FATAL, ERROR, WARN, WARNING, INFO, DEBUG, NOTSET]
        :return: A new instance of `Logger` with the configured name and log level.
        """
        self.name = name

        self._logger = _get_logging_logger(name=self.name)

        # Avoid overriding a previously-set  level when this logger is called up from cache
        if self._logger.level == logging.NOTSET:
            self._logger.setLevel(level=level.as_logging_module_level)

    def _add_handler(self, handler, msg_format: LogFormat, level: LogLevel = DEFAULT_LOG_LEVEL) -> None:
        msg_format_str = msg_format.build()
        formatter = logging.Formatter(fmt=msg_format_str)
        handler.setFormatter(fmt=formatter)

        # Need to adjust the parent logger to the lowest level requested
        if _is_lower_log_level(level=level.as_logging_module_level, other_level=self._logger.level):
            self._logger.setLevel(level=level.as_logging_module_level)

        handler.setLevel(level=level.as_logging_module_level)

        self._logger.addHandler(hdlr=handler)

    def log_to_console(self, level: LogLevel = DEFAULT_LOG_LEVEL,
                       msg_format: LogFormat = DEFAULT_CONSOLE_FORMAT) -> None:
        """Adds a console handler to a logger."""
        self._add_handler(handler=logging.StreamHandler(), msg_format=msg_format, level=level)

    def log_to_file(
            self,
            folder_path: str,
            file_name: str = None,
            level: LogLevel = DEFAULT_LOG_LEVEL,
            msg_format: LogFormat = DEFAULT_FILE_FORMAT,
            log_size: int = DEFAULT_LOG_MAX_BYTES,
            num_of_logs: int = DEFAULT_LOG_BACKUP_COUNT,
            encoding: str = 'utf-8',
    ) -> None:
        """Adds a file handler to a logger."""
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Splitting on the period assumes the user specified `__name__` so we can get
        # the root package name for log filenames, otherwise we'll just use the name.
        if not file_name:
            file_name = self._logger.name.split('.')[0] + '.log'

        log_file_path = os.path.join(folder_path, file_name)

        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file_path,
            maxBytes=log_size,
            backupCount=num_of_logs,
            encoding=encoding,
        )

        self._add_handler(handler=file_handler, msg_format=msg_format, level=level)

    def fatal(self, message: str) -> None:
        """
        Alias for critical(), considered deprecated.
        """
        self.critical(message=message)

    def critical(self, message: str) -> None:
        self._logger.critical(msg=message)

    def error(self, message: str) -> None:
        self._logger.error(msg=message)

    def warning(self, message: str) -> None:
        self._logger.warning(msg=message)

    def warn(self, message: str) -> None:
        """
        Alias for warning(), considered deprecated.
        """
        self.warning(message=message)

    def info(self, message: str) -> None:
        self._logger.info(msg=message)

    def debug(self, message: str) -> None:
        self._logger.debug(msg=message)


def _get(name: str) -> Logger:
    """
    Get a logger instance by name.
    You should instead consider making an instance of Logger and keeping track of it to avoid unnecessary overhead.
    """
    return Logger(name=name)  # Will build a new instance with the same internal logger (if it exists)


def fatal(message: str, specific_logger: Optional[str] = None):
    """
    Alias for critical(), considered deprecated.

    You should instead consider making an instance of Logger and keeping track of it to avoid unnecessary overhead.
    """
    critical(message=message, specific_logger=specific_logger)


def critical(message: str, specific_logger: Optional[str] = None):
    """
    You should instead consider making an instance of Logger and keeping track of it to avoid unnecessary overhead.
    """
    _get(specific_logger if specific_logger else DEFAULT_LOGGER_NAME).critical(message=message)


def error(message: str, specific_logger: Optional[str] = None):
    """
    You should instead consider making an instance of Logger and keeping track of it to avoid unnecessary overhead.
    """
    _get(specific_logger if specific_logger else DEFAULT_LOGGER_NAME).error(message=message)


def warning(message: str, specific_logger: Optional[str] = None):
    """
    You should instead consider making an instance of Logger and keeping track of it to avoid unnecessary overhead.
    """
    _get(specific_logger if specific_logger else DEFAULT_LOGGER_NAME).warning(message=message)


def warn(message: str, specific_logger: Optional[str] = None):
    """
    Alias for warning(), considered deprecated.

    You should instead consider making an instance of Logger and keeping track of it to avoid unnecessary overhead.
    """
    warning(message=message, specific_logger=specific_logger)


def info(message: str, specific_logger: Optional[str] = None):
    """
    You should instead consider making an instance of Logger and keeping track of it to avoid unnecessary overhead.
    """
    _get(specific_logger if specific_logger else DEFAULT_LOGGER_NAME).info(message=message)


def debug(message: str, specific_logger: Optional[str] = None):
    """
    You should instead consider making an instance of Logger and keeping track of it to avoid unnecessary overhead.
    """
    _get(specific_logger if specific_logger else DEFAULT_LOGGER_NAME).debug(message=message)
