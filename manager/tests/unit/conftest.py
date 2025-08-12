"""
Shared pytest configuration and fixtures.

This file automatically applies mocks to external dependencies for all tests
in the suite, preventing side effects during import or execution.
"""

import pytest
from manager import database, main


class TestConfig:
    """Configuration for tests. Uses in-memory SQLite and disables tracking."""

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


@pytest.fixture(scope="function")
def app():
    """Create and configure a new app instance for each test."""
    flask_app = main.create_app(test_config=TestConfig)

    with flask_app.app_context():
        database.db.create_all()

    yield flask_app


@pytest.fixture(scope="function")
def client(app):  # pylint: disable=redefined-outer-name
    """
    Provide a test client for the Flask app.

    Allows sending HTTP requests to the application
    without running a real server.
    """
    return app.test_client()
