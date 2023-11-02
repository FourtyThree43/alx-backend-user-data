#!/usr/bin/env python3
""" Module filtered_logger
"""
from mysql.connector import Error
from typing import List
import logging
import mysql.connector
import os
import re

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Function that returns the log message obfuscated"""
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    """Function that returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Function that returns a connector to the database"""
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "my_db")
    db_port = os.getenv('PERSONAL_DATA_DB_PORT', 3306)  # Default MySQL port

    connector = None

    try:
        connector = mysql.connector.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name,
        )
    except Error as e:
        print(f"The error '{e}' occurred")

    return connector


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        """Constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Function that filters values in incoming log records using
        filter_datum. Values for fields in fields should be filtered.
        """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            fields=self.fields,
            redaction=self.REDACTION,
            message=message,
            separator=self.SEPARATOR,
        )


def main():
    """ Main function
    """
    columns = [
        "name", "email", "phone", "ssn", "password", "ip", "last_login",
        "user_agent"
    ]
    fields = ','.join(columns)
    query = f"SELECT {fields} FROM users;"

    info_logger = get_logger()
    connection = get_db()

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            record = map(lambda x: '{}={}'.format(x[0], x[1]),
                         zip(columns, row))
            msg = '{};'.format('; '.join(list(record)))
            info_logger.info(msg)


if __name__ == "__main__":
    main()
