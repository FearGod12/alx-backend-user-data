#!/usr/bin/env python3
"""the filtered logger module
"""

import re
from typing import List
import logging
import os

import mysql
from mysql.connector.connection import MySQLConnection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """In this task, you will connect to a secure holberton
    database to read a users table. The database is protected by a
    username and password that are set as environment variables on the
    server named PERSONAL_DATA_DB_USERNAME (set the default as “root”),
    PERSONAL_DATA_DB_PASSWORD (set the default as an empty string) and
    PERSONAL_DATA_DB_HOST (set the default as “localhost”).
    The database name is stored in PERSONAL_DATA_DB_NAME."""
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    passwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db = os.getenv("PERSONAL_DATA_DB_NAME")

    database = MySQLConnection(host=host, user=user, password=passwd,
                               database=db)
    return database


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
