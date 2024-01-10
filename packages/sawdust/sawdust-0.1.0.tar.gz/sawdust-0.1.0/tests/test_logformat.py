from sawdust import LogFormat


def test_include_time():
    formatter = LogFormat()

    formatter.include_time()

    assert '%(asctime)s' in formatter.build()


def test_include_level():
    formatter = LogFormat()

    formatter.include_level()

    assert '%(levelname)s' in formatter.build()


def test_include_calling_function():
    formatter = LogFormat()

    formatter.include_calling_function()

    assert '%(module)s.%(funcName)s' in formatter.build()


def test_include_process_name():
    formatter = LogFormat()

    formatter.include_process_name()

    assert '%(processName)s' in formatter.build()


def test_include_logger_name():
    formatter = LogFormat()

    formatter.include_logger_name()

    assert '%(name)s' in formatter.build()


def test_build():
    formatter = LogFormat()

    formatter.include_time()
    formatter.include_level()
    formatter.include_calling_function()
    formatter.include_process_name()
    formatter.include_logger_name()

    log_format_string = formatter.build()

    assert '%(asctime)s' in log_format_string
    assert '%(levelname)s' in log_format_string
    assert '%(module)s.%(funcName)s' in log_format_string
    assert '%(processName)s' in log_format_string
    assert '%(name)s' in log_format_string
