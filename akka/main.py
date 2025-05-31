import configparser

from flask import Flask, render_template, request, redirect, url_for
import request
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False


@app.route("/")
def show_environments():
    """Show Environments Page"""
    config = configparser.ConfigParser()
    config.read("environments.cfg")
    environments = []
    for section in config.sections():
        env = {"name": section}
        env.update(config[section])
        environments.append(env)
    return render_template("environments.html", environments=environments)


@app.route("/request-runner", methods=["GET", "POST"])
def request_runner():
    form = request.RequestForm()
    if form.validate_on_submit():
        environment_name = form.environment_name.data
        project_group = form.project_group.data
        tags = form.tags.data

        print(
            f"Requested GitLab Runner - Environment: {environment_name}, Group: {project_group}, Tags: {tags}"
        )

        return redirect(url_for("success"))

    return render_template("request_runner.html", form=form)


@app.route("/success")
def success():
    return "GitLab Runner request submitted successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
