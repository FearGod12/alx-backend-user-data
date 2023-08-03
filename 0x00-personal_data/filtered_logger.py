#!/usr/bin/env python3
"""the filtered logger module
"""

import re
from typing import List, Iterable
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Replacing """
    for entry in fields:
        message = re.sub(rf"{entry}=(.*?){separator}",
                         f'{entry}={redaction}{separator}', message)
    return message


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
