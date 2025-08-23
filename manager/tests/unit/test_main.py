"""
Unit tests for the Flask app factory in main.py.

This module tests:
- App creates with default config.
- App uses provided test config.
- Routes register correctly.

Author: Liora Milbaum
"""

from unittest import mock

from manager import main


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

        class TestConfig:
            """Configuration for tests. Uses in-memory SQLite and disables tracking."""

            SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            TESTING = True

        app = main.create_app(test_config=TestConfig)

        mock_init.assert_called_once_with(app)
        mock_create_all.assert_called_once()

        assert app.config["TESTING"] is True
        assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_home_route(client):
    """GET / should return the home page HTML."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Welcome to the Akka App" in html
    assert 'href="' in html
    assert "Request a Runner" in html
    assert "View Runners" in html


def test_request_endpoint_exists(app):
    """Make sure /runners/request URL is registered."""
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    assert "/runners/request" in rules


def test_request_runner_success(client, app):
    """POST /runners/request should request a new Runner record into the DB."""
    with app.app_context():
        main.database.db.create_all()

    payload = {
        "name": "test-runner",
        "gitlab_group_id": "https://gitlab.com/test-group",
        "tags": "test-tag",
    }
    response = client.post("/runners/request", json=payload)

    assert response.status_code == 201


def test_request_runner_bad_payload(client):
    """POST /runners/request with missing fields should return 400."""
    response = client.post("/runners/request", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
