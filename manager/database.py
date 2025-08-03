"""
Provide and configure the SQLAlchemy database extension.

This module initializes the global `db` instance using Flask‑SQLAlchemy.

Author: Liora Milbaum
"""

import os

import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


def get_db_uri():
    """
    Build the SQLAlchemy database URI from environment variables.

    Returns:
        str: A PostgreSQL connection URI in the format
        'postgresql://<user>:<password>@<host>:5432/<database>'.

    """
    DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    DB_NAME = os.environ.get("POSTGRES_DB", "mydb")
    DB_USER = os.environ.get("POSTGRES_USER", "user")
    DB_PASS = os.environ.get("POSTGRES_PASSWORD", "password")
    return f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"


def init_db(app):
    """Initialize DB by creating tables."""
    with app.app_context():
        db.create_all()
