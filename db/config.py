"""
Shared PostgreSQL configuration helper for multiple microservices.

This module provides a single source of truth for constructing the
PostgreSQL connection URI using environment variables. Both microservices
in the monorepo can import and reuse this helper to ensure consistent
database connectivity without duplicating configuration logic.

Environment Variables:
- POSTGRES_HOST: hostname of the PostgreSQL server (default: "localhost")
- POSTGRES_DB: database name (default: "mydb")
- POSTGRES_USER: database username (default: "user")
- POSTGRES_PASSWORD: database password (default: "password")

Example:
    from db.config import get_postgres_uri

    DATABASE_URI = get_postgres_uri()

"""

import os


def get_postgres_uri() -> str:
    """Return PostgreSQL URI from environment variables (single source of truth)."""
    host = os.environ.get("POSTGRES_HOST", "localhost")
    db = os.environ.get("POSTGRES_DB", "mydb")
    user = os.environ.get("POSTGRES_USER", "user")
    password = os.environ.get("POSTGRES_PASSWORD", "password")
    return f"postgresql://{user}:{password}@{host}/{db}"
