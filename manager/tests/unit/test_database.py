"""
Unit tests for the database module.

Tests:
- Environment variables are read correctly.
- SQLAlchemy engine is created with the expected URL.
- init_db() calls metadata.create_all() as expected.

Author: Liora Milbaum
"""

from unittest import mock

from manager import database


def test_get_db_uri(monkeypatch):
    """Test that get_db_uri builds the URI correctly."""
    monkeypatch.setenv("POSTGRES_HOST", "db_host")
    monkeypatch.setenv("POSTGRES_DB", "mydb")
    monkeypatch.setenv("POSTGRES_USER", "myuser")
    monkeypatch.setenv("POSTGRES_PASSWORD", "mypass")

    uri = database.get_db_uri()
    assert uri == "postgresql://myuser:mypass@db_host:5432/mydb"


def test_init_db_calls_create_all():
    """Test that init_db calls db.create_all()."""
    with mock.patch.object(database.db, "create_all") as mock_create_all:
        app = mock.Mock()
        app_ctx = mock.MagicMock()
        app.app_context.return_value = app_ctx

        database.init_db(app)

        app.app_context.assert_called_once()
        app_ctx.__enter__.assert_called_once()
        mock_create_all.assert_called_once()
