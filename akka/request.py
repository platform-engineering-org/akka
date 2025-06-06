from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
import re
from wtforms.validators import DataRequired, Length, Regexp

def validate_comma_list(form, field):
    items = [item.strip() for item in field.data.split(',')]
    pattern = re.compile(r'^[a-zA-Z\-]+$')
    for item in items:
        if not (2 <= len(item) <= 20):
            raise ValidationError(f'Tag "{item}" must be between 2 and 20 characters')
        if not pattern.fullmatch(item):
            raise ValidationError(f'Tag "{item}" contains invalid characters')


class RequestForm(FlaskForm):
    environment_name = StringField(
        'Environment Name',
        validators=[
            DataRequired(),
            Length(min=2, max=20),
            Regexp(r'^[a-zA-Z0-9\-]+$', message="Only letters, numbers and dashes are allowed")
        ]
    )
    project_group = StringField(
        'Project Group',
        validators=[
            DataRequired(),
            Length(min=2, max=50),
            Regexp(r'^[a-zA-Z0-9\-]+(\/[a-zA-Z0-9\-]+)*$', message="Project group must contain only letters, numbers, dashes, and slashes (no // or trailing slash)")
        ]
    )
    tags = StringField('Tags', validators=[validate_comma_list])
