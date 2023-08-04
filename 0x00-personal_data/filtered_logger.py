#!/usr/bin/env python3
"""the filtered logger module
"""

import re
from typing import List, Iterable
import logging

PII_FIELDS = ("name", "email", "phone", "ssn", "ip")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Replacing """
    for entry in fields:
        message = re.sub(rf"{entry}=(.*?){separator}",
                         f'{entry}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """return a logger that alogs message to """
    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """the class constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats the record overriding the default formatter"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
