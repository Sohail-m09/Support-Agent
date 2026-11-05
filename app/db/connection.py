"""
connection.py - opens a connection to the Postgres database on Neon.

Why it exists: every file that talks to the database gets its connection
from here, so the connection settings live in one place.
"""
import time
import importlib

psycopg = importlib.import_module("psycopg")

from app import config


def get_connection():
    """Open a database connection. Tries twice, because Neon may be waking up."""
    for attempt in (1, 2):
        try:
            return psycopg.connect(config.DATABASE_URL, connect_timeout=15)
        except psycopg.OperationalError:
            if attempt == 2:
                raise
            time.sleep(3)  # give a sleeping database a moment to wake up