"""
Unit tests for the runners blueprint.

Tests:
- /runners/list returns runners.
- /runners/request handles JSON POST.
- /runners/request fails with bad payload.
- /runners/success returns success message.

Author: Liora Milbaum
"""

import flask
import pytest
from manager import database, models


def test_list_runners(client, app):
    """Test GET /runners/list returns runners page."""
    with app.app_context():
        r = models.Runner(name="r1", gitlab_group_id="group/1", tags="tag1")
        database.db.session.add(r)
        database.db.session.commit()

    response = client.get("/runners/list")
    assert response.status_code == 200
    assert b"r1" in response.data  # Assumes template renders runner name


def test_request_runner_json_success(client, app):
    """POST /runners/request with JSON creates a runner."""
    payload = {
        "name": "runner-json",
        "gitlab_group_id": "group/json",
        "tags": "tag1,tag2",
    }
    response = client.post("/runners/request", json=payload)

    assert response.status_code == 201
    assert b"requested successfully" in response.data

    with app.app_context():
        saved = models.Runner.query.filter_by(gitlab_group_id="group/json").first()
        assert saved is not None


def test_request_runner_json_bad_payload(client):
    """POST /runners/request with bad JSON returns 400."""
    payload = {"name": "incomplete"}
