"""
Provide database models for the application.

Defines the core models used for persisting and querying application data:
- Runner: represents the self hosted runner.

Classes:
    Runner: A GitLab Self Hosted Runner

Author: Liora Milbaum
"""

from . import database


class Runner(database.db.Model):
    """Self Hosted Runner."""

    __tablename__ = "runners"

    id = database.db.Column(database.db.Integer, primary_key=True)
    name = database.db.Column(database.db.String(128), nullable=False)
    gitlab_group_id = database.db.Column(
        database.db.String(256), nullable=False, unique=True
    )
    tags = database.db.Column(database.db.String(256), nullable=False, unique=False)
