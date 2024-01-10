import logging
from logging import Logger

from .logger import get_log, get_logpath, get_logpaths, getLogger, load_log
from .models import Event, Log

__version__ = "0.3.0"

CRITICAL = logging.CRITICAL
FATAL = CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET
