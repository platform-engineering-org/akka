"""
Application configuration module.

Defines configuration classes for different environments (default, testing, etc.).
The default `Config` class includes settings for SQLAlchemy, secret keys,
and other Flask extensions. Values can be overridden via environment variables.

Author: Liora Milbaum
"""

import os

DB_HOST = os.environ.get("POSTGRES_HOST")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")


class Config:
    """
    Base configuration class for the Flask application.

    Provides default settings including:
    - Database URI (from the DATABASE_URL environment variable or a default fallback)
    - SQLAlchemy behavior
    - Secret key for session management

    Intended to be extended for environment-specific configurations (e.g., testing, production).
    """

    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
