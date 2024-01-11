"""Unit logger."""
import logging
import json

class JSONFormatter(logging.Formatter):
    """Custom json formatter."""

    def format(self, record):
        """Make logs format."""
        log_record = {
            'asctime': self.formatTime(record, self.datefmt),
            'levelname': record.levelname,
            'message': record.getMessage(),
        }
        return json.dumps(log_record, ensure_ascii=False)

class Logging():
    """Loggin class."""

    def __init__(self, logger_name):
        """Class desinger."""
        self.logger_name = logger_name
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.INFO)
        formatter = JSONFormatter()
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, level, message, *args):
        """Log method."""
        self.logger.log(level, message, *args)

    def info(self, message, *args):
        """INFO logging level."""
        self.log(logging.INFO, message, *args)

    def debug(self, message, *args):
        """DEBUG logging level."""
        self.log(logging.DEBUG, message, *args)

    def warning(self, message, *args):
        """WARNING logging level."""
        self.log(logging.WARNING, message, *args)

    def error(self, message, *args):
        """ERROR logging level."""
        self.log(logging.ERROR, message, *args)

    def critical(self, message, *args):
        """CRITICAL logging level."""
        self.log(logging.CRITICAL, message, *args)
