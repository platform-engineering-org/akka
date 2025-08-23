"""
Provide the Flask blueprint for runners routes.

Author: Liora Milbaum
"""

import flask

from . import database, forms, models

bp = flask.Blueprint("runners", __name__, url_prefix="/runners")


@bp.route("/list")
def list_runners():
    """
    Render the environments overview page.

    Reads environment configurations from 'environments.cfg' and
    passes the list of environments with their details to the template.
    """
    runners = models.Runner.query.all()
    return flask.render_template("runners.html", runners=runners)


@bp.route("/request", methods=["GET", "POST"])
def request_runner():
    """
    Handle the GitLab Runner request form.

    - On GET: Render the request form.
    - On POST: Validate submitted form data.
      If valid, process the request and redirect to the success page.
      Otherwise, re-render the form with errors.

    The form captures environment name, project group, and optional tags.
    """
    if flask.request.is_json:
        data = flask.request.get_json()
        name = data.get("name")
        gitlab_group_id = data.get("gitlab_group_id")
        tags = data.get("tags")

        if not name or not gitlab_group_id or not tags:
            return flask.jsonify({"error": "Missing required fields"}), 400

        new_runner = models.Runner(
            name=name, gitlab_group_id=gitlab_group_id, tags=tags
        )
        database.db.session.add(new_runner)
        database.db.session.commit()
        return flask.jsonify(
            {"message": f"Runner '{new_runner}' requested successfully"}
        ), 201
    else:
        form = forms.RequestForm()
        if form.validate_on_submit():
            new_runner = models.Runner(
                name=form.name.data,
                gitlab_group_id=form.gitlab_group_id.data,
                tags=form.tags.data,
            )
            database.db.session.add(new_runner)
            database.db.session.commit()
            return flask.redirect(flask.url_for("runners.success"))

    return flask.render_template("request_runner.html", form=form)


@bp.route("/success", methods=["GET"])
def success():
    """Success page."""
    return flask.render_template("success.html")
