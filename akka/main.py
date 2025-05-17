import configparser

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def show_environments():
    """Show Environments Page"""
    config = configparser.ConfigParser()
    config.read('environments.cfg')
    environments = []
    for section in config.sections():
        env = {'name': section}
        env.update(config[section])
        environments.append(env)
    return render_template('environments.html', environments=environments)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
