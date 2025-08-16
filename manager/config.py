"""
Application configuration module.

Defines configuration classes for different environments (default, testing, etc.).
The default `Config` class includes settings for SQLAlchemy, secret keys,
and other Flask extensions. Values can be overridden via environment variables.

Author: Liora Milbaum
"""

from db import config


class Config:
    """
    Base configuration class for the Flask application.

    Provides default settings including:
    - Database URI (from centralized helper)
    - SQLAlchemy behavior
    - Secret key for session management
    """

    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        """
        Initialize the configuration instance.

        Reads the PostgreSQL connection URI from environment variables via
        the shared `get_postgres_uri()` helper. This allows tests to
        monkeypatch environment variables before instantiation.
        """
        self.SQLALCHEMY_DATABASE_URI = config.get_postgres_uri()
