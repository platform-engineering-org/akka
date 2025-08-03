"""
Unit tests for the Flask app factory in main.py.

Tests:
- App creates with default config.
- App uses provided test config.
- App context initializes DB.
- Routes register correctly.

Author: Liora Milbaum
"""

from unittest import mock

from manager import main
from manager.tests.unit.conftest import TestConfig


def test_create_app_default():
    """App should load default config if test_config not provided."""
    with (
        mock.patch("manager.database.db.init_app") as mock_init,
        mock.patch("manager.database.db.create_all") as mock_create_all,
    ):
        app = main.create_app()

        mock_init.assert_called_once_with(app)
        mock_create_all.assert_called_once()

        assert "SQLALCHEMY_DATABASE_URI" in app.config


def test_create_app_with_test_config():
    """App should use given test_config."""
    with (
        mock.patch("manager.database.db.init_app") as mock_init,
        mock.patch("manager.database.db.create_all") as mock_create_all,
    ):
        app = main.create_app(test_config=TestConfig)

        mock_init.assert_called_once_with(app)
        mock_create_all.assert_called_once()

        assert app.config["TESTING"] is True
        assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_home_route(client):
    """GET / should return welcome JSON."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["message"] == "Welcome to the Akka app!"
