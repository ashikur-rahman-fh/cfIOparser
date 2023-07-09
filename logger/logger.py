"""
    File: logger.py
    Author: Ashikur Rahman
    Description: Logger module that provides different logging behaviour
"""

import sys
from cfsys import cfsys
from colorer.colorer import colored_text


class LogType:
    """Specify the log types"""
    FETAL       = 'FETAL'
    ERROR       = 'ERROR'
    SUCCESS     = 'SUCCESS'
    WARNING     = 'WARNING'
    INFO        = 'INFO'

class LogLevel:
    """Specify the level of the logs"""
    FETAL       = 4
    ERROR       = 3
    SUCCESS     = 2
    WARNING     = 1
    INFO        = 0


class LogColor:
    """Log colors"""
    FETAL       = 'red'
    ERROR       = 'red'
    SUCCESS     = 'green'
    WARNING     = 'yellow'
    INFO        = 'cyan'

class LogColorAttr:
    FETAL       = ['bold']


class Logger:
    """Actual logger singleton class than determine if the log should be displayed or not"""
    def __init__(self, log_level = LogLevel.SUCCESS) -> None:
        self.log_level = log_level

    def __new__(cls):
        if not hasattr(cls, 'logger'):
            cls.logger = super(Logger, cls).__new__(cls)

        return cls.logger

    def set_log_level(self, log_level):
        """Modify the current log level"""
        self.log_level = log_level

    def display(self, log_type, log_message):
        """display the log based on the level"""
        if self.log_level > getattr(LogLevel, str(log_type)):
            return

        current_time = cfsys.get_current_time()
        log_prefix = self.normalize_log_prefix(log_type)
        colored_prefix = colored_text(log_prefix, color=getattr(LogColor, log_type), attrs=getattr(LogColorAttr, log_type, None))

        display_text = f"{colored_prefix:10} {current_time}    {self.normalize_log_message(log_message)}."
        print(display_text)

    def normalize_log_message(self, message):
        """Normalized the log message and strip extra characters"""
        return str(message).strip('. \n \r \t')

    def normalize_log_prefix(self, prefix):
        """Normalize and format the log prefix"""
        nomalized_text = str(prefix).strip('. : \n \t \r') + ":"

        return f"{nomalized_text:10}"

__logger = Logger()

def set_log_level(log_level):
    """Set log level api"""
    __logger.set_log_level(log_level=log_level)

def fetal(message):
    """Fetal log api"""
    __logger.display(LogType.FETAL, message)
    sys.exit(-1)

def error(message):
    """Error log api"""
    __logger.display(LogType.ERROR, message)

def success(message):
    """Success log api"""
    __logger.display(LogType.SUCCESS, message)

def warning(message):
    """Warning log api"""
    __logger.display(LogType.WARNING, message)

def info(message):
    """Info log api"""
    __logger.display(LogType.INFO, message)
