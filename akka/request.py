"""
Defines the `RequestForm` Flask-WTF form and related validators for environment provisioning requests.

The module includes:
- `RequestForm`: A form class with fields for environment name, project group, and tags.
- `validate_comma_list`: Custom validator for comma-separated tag lists ensuring proper format.

Form field validations enforce naming conventions and character restrictions to maintain data consistency
for environment provisioning workflows.

Author: Liora Milbaum
"""

import re

from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp


def validate_comma_list(form, field):
    """
    Validate a comma-separated list of tags.

    Each tag must:
        - Be between 2 and 20 characters long (inclusive)
        - Contain only letters (a–z, A–Z) and dashes (`-`)

    Strips leading/trailing whitespace from each tag before validation.

    Raises:
        ValidationError: If any tag is too short/long or contains invalid characters.

    """
    items = [item.strip() for item in field.data.split(",")]
    pattern = re.compile(r"^[a-zA-Z\-]+$")
    for item in items:
        if not (2 <= len(item) <= 20):
            raise ValidationError(f'Tag "{item}" must be between 2 and 20 characters')
        if not pattern.fullmatch(item):
            raise ValidationError(f'Tag "{item}" contains invalid characters')


class RequestForm(FlaskForm):
    """
    Form for submitting environment provisioning requests.

    Fields:
        environment_name (StringField): Name of the environment to be created.
            - Required
            - 2–20 characters
            - Must consist of letters, numbers, and dashes only

        project_group (StringField): Project group path associated with the environment.
            - Required
            - 2–50 characters
            - Allows letters, numbers, dashes, and forward slashes
            - Must not contain double slashes or a trailing slash

        tags (StringField): Optional comma-separated list of tags.
            - Validated using a custom `validate_comma_list` validator
    """

    environment_name = StringField(
        "Environment Name",
        validators=[
            DataRequired(),
            Length(min=2, max=20),
            Regexp(
                r"^[a-zA-Z0-9\-]+$",
                message="Only letters, numbers and dashes are allowed",
            ),
        ],
    )
    project_group = StringField(
        "Project Group",
        validators=[
            DataRequired(),
            Length(min=2, max=50),
            Regexp(
                r"^[a-zA-Z0-9\-]+(\/[a-zA-Z0-9\-]+)*$",
                message="Project group must contain only letters, numbers, dashes, and slashes (no // or trailing slash)",
            ),
        ],
    )
    tags = StringField("Tags", validators=[validate_comma_list])
