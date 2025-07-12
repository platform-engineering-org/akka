"""
Unit tests for Flask-based application.

This module contains pytest-based tests for the Flask application defined in
manager.app. It verifies the following behaviors:
  - The root route ("/") correctly reads and displays environment configurations.
  - The GET and POST handlers for "/request-runner" respond appropriately,
    handling both valid and invalid form submissions.
  - The "/success" route renders the expected success message.

The tests utilize monkeypatching to simulate configuration parsing and form
validations, ensuring behavior is tested in isolation.
"""

import configparser

import pytest
from manager import forms
from manager import main as flask_app


@pytest.fixture
def client():
    """
    Provide a Flask test client configured for testing.

    Yields:
        A Flask test client instance with TESTING mode enabled.

    """
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as client:
        yield client


def test_show_environments(monkeypatch, client):
    """
    Tests that the root ("/") route displays available environments.

    Mocks ConfigParser to simulate a config file with two sections:
    - "dev" with url "http://example.com"
    - "prod" with url "http://prod.com"

    Verifies the route responds with status 200 and that the rendered
    template includes the word "environments".
    """

    def mock_read(self, filename):
        pass  # bypass actual file reading

    def mock_sections(self):
        return ["dev", "prod"]

    def mock_getitem(self, key):
        return (
            {"url": "http://example.com"}
            if key == "dev"
            else {"url": "http://prod.com"}
        )

    monkeypatch.setattr(configparser.ConfigParser, "read", mock_read)
    monkeypatch.setattr(configparser.ConfigParser, "sections", mock_sections)
    monkeypatch.setattr(configparser.ConfigParser, "__getitem__", mock_getitem)

    response = client.get("/")
    assert response.status_code == 200
    assert b"Environments" in response.data


def test_request_runner_get(client):
    """
    Tests that a GET request to '/request-runner' returns the form.

    Verifies a 200 status code and checks that the form or
    submission prompt appears in the response content.
    """
    response = client.get("/request-runner")
    assert response.status_code == 200
    assert b"form" in response.data or b"Request" in response.data


def test_request_runner_post_valid(monkeypatch, client):
    """Tests that a valid POST to '/request-runner' redirects to '/success'."""

    class DummyField:
        label = "Label"
        data = "dummy"

        def __call__(self, *args, **kwargs):
            return ""

    class DummyForm:
        environment_name = DummyField()
        project_group = DummyField()
        tags = DummyField()

        def validate_on_submit(self):
            return True

        def hidden_tag(self):
            return ""

    monkeypatch.setattr(forms, "RequestForm", lambda: DummyForm())

    response = client.post("/request-runner", data={})
    assert response.status_code == 302
    assert "/success" in response.headers["Location"]


def test_request_runner_post_invalid(monkeypatch, client):
    """Tests that an invalid POST to '/request-runner' re-renders the form."""

    class DummyField:
        label = "Label"

        def __call__(self, *args, **kwargs):
            return ""

    class DummyForm:
        environment_name = DummyField()
        project_group = DummyField()
        tags = DummyField()

        def validate_on_submit(self):
            return False

        def hidden_tag(self):
            return ""

    monkeypatch.setattr(forms, "RequestForm", lambda: DummyForm())

    response = client.post("/request-runner", data={})
    assert response.status_code == 200


def test_success(client):
    """
    Tests that accessing '/success' returns a confirmation message.

    Verifies a 200 status code and that the expected success message
    appears in the response body.
    """
    response = client.get("/success")
    assert response.status_code == 200
    assert b"GitLab Runner request submitted successfully" in response.data
