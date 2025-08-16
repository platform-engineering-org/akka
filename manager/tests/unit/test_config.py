"""
Unit tests for the application configuration module.

Tests Config class and get_postgres_uri helper for correct environment variable handling.

Author: Liora Milbaum
"""

from db import config as db_config
from manager import config as manager_config

# -------------------- get_postgres_uri Tests -------------------- #


def test_get_postgres_uri_defaults(monkeypatch):
    """Verify that get_postgres_uri() returns default values when no environment variables are set."""
    monkeypatch.delenv("POSTGRES_HOST", raising=False)
    monkeypatch.delenv("POSTGRES_DB", raising=False)
    monkeypatch.delenv("POSTGRES_USER", raising=False)
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)

    uri = db_config.get_postgres_uri()
    expected_uri = "postgresql://user:password@localhost/mydb"
    assert uri == expected_uri


def test_get_postgres_uri_custom(monkeypatch):
    """Verify that get_postgres_uri() correctly reflects custom environment variables."""
    monkeypatch.setenv("POSTGRES_HOST", "db-server")
    monkeypatch.setenv("POSTGRES_DB", "testdb")
    monkeypatch.setenv("POSTGRES_USER", "admin")
    monkeypatch.setenv("POSTGRES_PASSWORD", "secret")

    uri = db_config.get_postgres_uri()
    expected_uri = "postgresql://admin:secret@db-server/testdb"
    assert uri == expected_uri


# -------------------- Config Class Tests -------------------- #


def test_config_db_uri_defaults(monkeypatch):
    """Verify Config.SQLALCHEMY_DATABASE_URI uses default values when no env vars are set."""
    monkeypatch.delenv("POSTGRES_HOST", raising=False)
    monkeypatch.delenv("POSTGRES_DB", raising=False)
    monkeypatch.delenv("POSTGRES_USER", raising=False)
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)

    cfg = manager_config.Config()
    expected_uri = "postgresql://user:password@localhost/mydb"
    assert cfg.SQLALCHEMY_DATABASE_URI == expected_uri


def test_config_db_uri_custom(monkeypatch):
    """Verify Config.SQLALCHEMY_DATABASE_URI correctly reflects custom PostgreSQL environment variables."""
    monkeypatch.setenv("POSTGRES_HOST", "db-server")
    monkeypatch.setenv("POSTGRES_DB", "testdb")
    monkeypatch.setenv("POSTGRES_USER", "admin")
    monkeypatch.setenv("POSTGRES_PASSWORD", "secret")

    cfg = manager_config.Config()
    expected_uri = "postgresql://admin:secret@db-server/testdb"
    assert cfg.SQLALCHEMY_DATABASE_URI == expected_uri


def test_config_defaults():
    """Verify other default Config settings."""
    cfg = manager_config.Config()
    assert cfg.WTF_CSRF_ENABLED is False
    assert cfg.SQLALCHEMY_TRACK_MODIFICATIONS is False
