"""
Unit tests for the SQLAlchemy database extension.

Tests database.db initialization and init_db() function with a minimal Flask app.

Author: Liora Milbaum
"""

from manager import database


def test_db_instance_initialization(app):
    """Verify that the SQLAlchemy db instance is correctly associated with the Flask app."""
    with app.app_context():
        # Ensure db.session works inside the app context
        assert database.db.session is not None
        assert str(database.db.engine.url).startswith("sqlite://")


def test_init_db_creates_tables(app):
    """Verify that database.init_db() successfully creates tables for models."""
    from sqlalchemy import Column, Integer, String

    class TestModel(database.db.Model):
        __tablename__ = "test_model"
        id = Column(Integer, primary_key=True)
        name = Column(String(50))

    database.init_db(app)
    assert "test_model" in database.db.metadata.tables
