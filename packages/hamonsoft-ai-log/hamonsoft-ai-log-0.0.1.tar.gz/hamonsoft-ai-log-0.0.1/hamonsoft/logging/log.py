import logging.handlers


class Log(logging.Logger):
    __format = '[%(process)s][%(threadName)-10s][%(asctime)-8s][%(levelname)-8s][%(module)-10s][%(funcName)-10s(%(lineno)-3s)] - %(message)s'
    __file_handler = None

    logging.basicConfig(level=logging.INFO,
                        datefmt='%H:%M:%S',
                        format=__format,
                        encoding="utf-8")

    __log = logging.getLogger(name="LogWriter")

    @staticmethod
    def set_log_level(level) -> None:
        levels = {
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
            "DEBUG": logging.DEBUG
        }
        Log.__log.setLevel(levels.get(level, logging.DEBUG))

    @staticmethod
    def set_log_file(file_name) -> None:
        Log.file_handler = logging.handlers.TimedRotatingFileHandler(filename=file_name,
                                                                     when='midnight',
                                                                     backupCount=0,
                                                                     interval=1,
                                                                     encoding='utf-8')
        Log.file_handler.setFormatter(logging.Formatter(fmt=Log.__format,
                                                        datefmt='%H:%M:%S',
                                                        style='%',
                                                        validate=True))
        Log.__log.addHandler(Log.file_handler)

    @staticmethod
    def remove_log_file() -> None:
        if Log.file_handler:
            Log.__log.removeHandler(Log.file_handler)
            Log.file_handler = None

    @staticmethod
    def set_log_name(log_name: str) -> None:
        Log.__log = logging.getLogger(log_name)

    @staticmethod
    def set_format(fmt=None, date_format='%H:%M:%S', style='%') -> None:
        Log.formatter = logging.Formatter(fmt=fmt,
                                          datefmt=date_format,
                                          style=style,
                                          validate=True)

    @staticmethod
    def info(msg, *args, **kwargs):
        Log.__log.info(msg, *args, **kwargs)

    @staticmethod
    def warning(msg, *args, **kwargs):
        Log.__log.warning(msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        Log.__log.error(msg, *args, **kwargs)

    @staticmethod
    def critical(msg, *args, **kwargs):
        Log.__log.critical(msg, *args, **kwargs)

    @staticmethod
    def debug(msg, *args, **kwargs):
        Log.__log.debug(msg, *args, **kwargs)

    @staticmethod
    def fatal(msg, *args, **kwargs):
        Log.__log.fatal(msg, *args, **kwargs)
