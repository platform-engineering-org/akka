"""
Main Flask application for managing environment configurations and GitLab Runner requests.

Uses Flask-WTF for form handling and validation.

Author: Liora Milbaum
"""

import flask

from manager import config, database, routes


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = flask.Flask(__name__)

    if test_config is None:
        app.config.from_object(config.Config())
    else:
        app.config.from_object(test_config)

    database.db.init_app(app)

    @app.route("/")
    def home():
        """Landing page for the Akka app."""
        return flask.render_template("home.html")

    app.register_blueprint(routes.bp)

    with app.app_context():
        database.db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
