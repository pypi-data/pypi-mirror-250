<div align="center">

# Sawdust

An even cuter little logger.

[![Build Status](https://github.com/nwithan8/sawdust/workflows/build/badge.svg)](https://github.com/nwithan8/sawdust/actions)
[![Coverage Status](https://coveralls.io/repos/github/nwithan8/sawdust/badge.svg?branch=main)](https://coveralls.io/github/nwithan8/sawdust?branch=main)
[![PyPi](https://img.shields.io/pypi/v/woodchips)](https://pypi.org/project/woodchips)
[![Licence](https://img.shields.io/github/license/nwithan8/sawdust)](LICENSE)

<img src="https://raw.githubusercontent.com/nwithan8/assets/main/src/sawdust/showcase.png" alt="Showcase">

</div>

> > Aren't logs just a bunch of woodchips?
>
> Aren't woodchips just a bunch of sawdust?

Sawdust is a re-implementation (improvement?) of [Woodchips](https://github.com/Justintime50/woodchips). This is largely
a joke (I know the Woodchips developer), but also a product of my inability to be satisfied with a product that does 90%
of what I expect, as well as my inability to not needlessly refactor things.

## Install

```bash
# Install tool
pip3 install sawdust

# Install locally
make install
```

## Usage

Create a `Logger` instance and start chipping/logging/dusting away!

```python
import sawdust

# Setup a new logger instance
logger = sawdust.Logger(
    name='my_logger_name',  # The name of your logger instance, often will be `__name__`
    level=sawdust.LogLevel.INFO,  # The log level you want to use
)

# Setup console logging
console_log_msg_format = sawdust.LogFormat()  # Only include the message in the console log
logger.log_to_console(level=sawdust.LogLevel.WARNING, msg_format=console_log_msg_format)

# Setup file logging
file_log_msg_format = sawdust.LogFormat().include_time().include_level().include_calling_function()  # Include the time, level, and calling function in the file log
logger.log_to_file(
    folder_path='path/to/log_files',
    file_name='my_log_file.log',
    level=sawdust.LogLevel.DEBUG,
    msg_format=file_log_msg_format,
    log_size=200000,  # Size of a single file in bytes
    num_of_logs=5,  # Number of log files to keep in the rotation
)

# Log a message (will be logged to console and a file based on the example from above)
logger.info('This is how to setup Sawdust!')

# Log a message without keeping a reference to the logger
sawdust.info('This is how to setup Sawdust!', specific_logger='my_logger_name')
```

### Available Log Levels

- `LogLevel.CRITICAL`
- `LogLevel.FATAL` (alias for `LogLevel.CRITICAL`, don't use this)
- `LogLevel.ERROR`
- `LogLevel.WARNING`
- `LogLevel.WARN` (alias for `LogLevel.WARNING`, don't use this)
- `LogLevel.INFO`
- `LogLevel.DEBUG`
- `LogLevel.NOTSET`

### Available Log Formats

Log elements will always appear in this order, with elements enabled or disabled accordingly:

`LOGGER_NAME - TIMESTAMP - LOG_LEVEL - PROCESS - FUNCTION: MESSAGE`

- `include_time()` - Include the time in the log
- `include_level()` - Include the log level in the log
- `include_calling_function()` - Include the calling function in the log
- `include_logger_name()` - Include the logger name in the log
- `include_process_name()` - Include the process name in the log
