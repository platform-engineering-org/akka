"""
Unit tests for the Runner database model.

Tests:
- Runner can be created and committed.
- Fields store correct values.
- Unique constraint on gitlab_group_id is enforced.

Author: Liora Milbaum
"""

import pytest
from manager import database, models


@pytest.fixture
def runner_data():
    """Sample runner data."""
    return {
        "name": "test-runner",
        "gitlab_group_id": "my/group/path",
        "tags": "tag1,tag2",
    }


def test_create_runner(app, runner_data):
    """Runner can be created and committed to DB."""
    with app.app_context():
        runner = models.Runner(**runner_data)
        database.db.session.add(runner)
        database.db.session.commit()

        saved = models.Runner.query.first()
        assert saved is not None
        assert saved.name == runner_data["name"]
        assert saved.gitlab_group_id == runner_data["gitlab_group_id"]
        assert saved.tags == runner_data["tags"]


def test_runner_gitlab_group_id_unique_constraint(app, runner_data):
    """Runner gitlab_group_id must be unique."""
    with app.app_context():
        r1 = models.Runner(**runner_data)
        database.db.session.add(r1)
        database.db.session.commit()

        r2 = models.Runner(**runner_data)
        database.db.session.add(r2)

        with pytest.raises(Exception):
            database.db.session.commit()
