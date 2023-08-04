#!/usr/bin/env python3
"""the filtered logger module
"""

import re
from typing import List
import logging
import os

import mysql
import mysql.connector

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
    """ Implement db conectivity
    """
    psw = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(
        host=host,
        database=db_name,
        user=username,
        password=psw)
    return conn


def main():
    """main function. and the only one to run when executed"""
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users;"
    cursor.execute(query)

    fields = ["name", "email", "phone", "ssn", "password"]
    for row in cursor:
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " + \
                  f"ssn={row[3]}; password={row[4]};ip={row[5]}; " + \
                  f"last_login={row[6]}; user_agent={row[7]};"
        print(message)

    cursor.close()
    conn.close()


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


if __name__ == "__main__":
    main()
