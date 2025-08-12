"""
Unit tests for the RequestForm and validate_comma_list validator.

Covers:
- Valid and invalid tag lists.
- RequestForm field constraints.

Author: Liora Milbaum
"""

import pytest
from manager.forms import RequestForm, validate_comma_list
from wtforms import Form, StringField, ValidationError


class DummyField:
    """Helper dummy to simulate WTForms field with `data`."""

    def __init__(self, data):
        """Initialize test case."""
        self.data = data


def test_validate_comma_list_valid(app):
    """Should accept valid comma-separated tags."""
    with app.app_context():
        field = DummyField("tag-one, tagTwo, tag-three")
        try:
            validate_comma_list(None, field)
        except ValidationError:
            pytest.fail("validate_comma_list() raised ValidationError unexpectedly!")


@pytest.mark.parametrize(
    "invalid_tags",
    [
        "a, validtag",  # too short
        "thisisaverylongtagname,ok",  # too long
        "goodtag, bad!tag",  # invalid chars
        "validtag, tag with space",  # spaces not allowed inside tag
    ],
)
def test_validate_comma_list_invalid(app, invalid_tags):
    """Should raise ValidationError on invalid tags."""
    with app.app_context():
        field = DummyField(invalid_tags)
        with pytest.raises(ValidationError):
            validate_comma_list(None, field)


def test_request_form_valid(app):
    """Should validate a properly formed RequestForm."""
    with app.app_context():
        form = RequestForm(
            data={
                "name": "env-123",
                "gitlab_group_id": "group/subgroup",
                "tags": "tag1,tag2",
            },
            meta={"csrf": False},
        )
        assert form.validate() is True


@pytest.mark.parametrize(
    "field, value",
    [
        ("name", ""),  # required
        ("name", "a"),  # too short
        ("name", "thisnameistoolongforthefield"),  # too long
        ("name", "bad name!"),  # invalid chars
        ("gitlab_group_id", ""),  # required
        ("gitlab_group_id", "a"),  # too short
        ("gitlab_group_id", "g" * 51),  # too long
        ("gitlab_group_id", "group//subgroup"),  # double slash
        ("gitlab_group_id", "group/subgroup/"),  # trailing slash
        ("tags", "bad tag!"),  # invalid tag by validator
    ],
)
def test_request_form_invalid(app, field, value):
    """Should fail for invalid field values."""
    with app.app_context():
        data = {"name": "valid-name", "gitlab_group_id": "valid/group", "tags": "tag1"}
        data[field] = value
        form = RequestForm(data=data, meta={"csrf": False})
        assert form.validate() is False
