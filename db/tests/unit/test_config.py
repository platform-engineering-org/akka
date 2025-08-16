"""
Unit tests for the shared PostgreSQL configuration helper.

This test suite verifies the behavior of `get_postgres_uri` in `db.config`.
It ensures that:

- Default environment variable values are used when none are set.
- Custom environment variable values are correctly reflected in the URI.

Uses pytest's `monkeypatch` fixture to temporarily modify environment variables
during tests.
"""

from db import config


def test_get_postgres_uri_defaults(monkeypatch):
    """Test that defaults are used when no environment variables are set."""
    # Clear environment variables for the test
    monkeypatch.delenv("POSTGRES_HOST", raising=False)
    monkeypatch.delenv("POSTGRES_DB", raising=False)
    monkeypatch.delenv("POSTGRES_USER", raising=False)
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)

    uri = config.get_postgres_uri()
    assert uri == "postgresql://user:password@localhost/mydb"


def test_get_postgres_uri_custom(monkeypatch):
    """Test that custom environment variables are correctly used."""
    monkeypatch.setenv("POSTGRES_HOST", "db-server")
    monkeypatch.setenv("POSTGRES_DB", "testdb")
    monkeypatch.setenv("POSTGRES_USER", "admin")
    monkeypatch.setenv("POSTGRES_PASSWORD", "secret")

    uri = config.get_postgres_uri()
    assert uri == "postgresql://admin:secret@db-server/testdb"
