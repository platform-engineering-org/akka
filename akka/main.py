import configparser

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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
    if request.method == "POST":
        environment = request.form["environment"]
        project_group = request.form["project_group"]
        tags = request.form["tags"]

        print(
            f"Requested GitLab Runner - Environment: {environment}, Group: {project_group}, Tags: {tags}"
        )

        return redirect(url_for("success"))

    return render_template("request_runner.html")


@app.route("/success")
def success():
    return "GitLab Runner request submitted successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
