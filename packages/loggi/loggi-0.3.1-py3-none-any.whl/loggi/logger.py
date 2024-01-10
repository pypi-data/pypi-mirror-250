import logging

from pathier import Pathier, Pathish

from loggi import models

root = Pathier(__file__).parent


def getLogger(name: str, path: Pathish = Pathier.cwd()) -> logging.Logger:
    """Get a configured `logging.Logger` instance for `name` with a file handler.

    The log file will be located in `path` at `path/{name}.log`.

    Default level is `INFO`.

    Logs are in the format: `{levelname}|-|{asctime}|-|{message}

    asctime is formatted as `%x %X`"""
    path = Pathier(path)
    path.mkdir()
    logger = logging.getLogger(name)
    # TODO: Add option for a stream handler
    logpath = path / f"{name}.log"
    handler = logging.FileHandler(logpath, encoding="utf-8")
    if handler.baseFilename not in [
        existing_handler.baseFilename
        for existing_handler in logger.handlers
        if isinstance(existing_handler, logging.FileHandler)
    ]:
        handler.setFormatter(
            logging.Formatter(
                "{levelname}|-|{asctime}|-|{message}",
                style="{",
                datefmt="%x %X",
            )
        )
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def load_log(logpath: Pathish) -> models.Log:
    """Return a `Log` object for the log file at `logpath`."""
    return models.Log.load_log(Pathier(logpath))


def get_logpaths(logger: logging.Logger) -> list[Pathier]:
    """Loop through the handlers for `logger` and return a list of paths for any handler of type `FileHandler`."""
    return [
        Pathier(handler.baseFilename)
        for handler in logger.handlers
        if isinstance(handler, logging.FileHandler)
    ]


def get_logpath(logger: logging.Logger) -> Pathier | None:
    """Search `logger.handlers` for a `FileHandler` that has a file stem matching `logger.name`.

    Returns `None` if not found."""
    for path in get_logpaths(logger):
        if path.stem == logger.name:
            return path


def get_log(logger: logging.Logger) -> models.Log | None:
    """Find the corresponding log file for `logger`, load it into a `models.Log` instance, and then return it.

    Returns `None` if a log file can't be found."""
    path = get_logpath(logger)
    if path:
        return load_log(path)


def close(logger: logging.Logger):
    """Removes and closes handlers for `logger`."""
    for handler in logger.handlers:
        logger.removeHandler(handler)
        handler.close()
