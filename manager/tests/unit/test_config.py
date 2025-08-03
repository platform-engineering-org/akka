"""
Unit tests for the config module.

Tests:
- Environment variables are read correctly.
- Config.SQLALCHEMY_DATABASE_URI is built as expected.

Author: Liora Milbaum
"""

import os

from manager import config


def test_sqlalchemy_database_uri(monkeypatch):
    """Test that Config.SQLALCHEMY_DATABASE_URI builds the expected URI."""
    monkeypatch.setenv("POSTGRES_HOST", "dbhost")
    monkeypatch.setenv("POSTGRES_DB", "mydb")
    monkeypatch.setenv("POSTGRES_USER", "myuser")
    monkeypatch.setenv("POSTGRES_PASSWORD", "mypass")

    # Reload module to pick up monkeypatched env vars
    import importlib

    importlib.reload(config)

    expected_uri = "postgresql://myuser:mypass@dbhost:5432/mydb"
    assert config.Config.SQLALCHEMY_DATABASE_URI == expected_uri


def test_csrf_disabled():
    """Test that WTF_CSRF_ENABLED is False by default."""
    assert config.Config.WTF_CSRF_ENABLED is False


def test_sqlalchemy_track_modifications_disabled():
    """Test that SQLAlchemy track modifications is False by default."""
    assert config.Config.SQLALCHEMY_TRACK_MODIFICATIONS is False
