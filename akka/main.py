from flask import Flask, render_template
import configparser

app = Flask(__name__)

@app.route('/')
def show_environments():
    config = configparser.ConfigParser()
    config.read('environments.cfg')
    environments = []
    for section in config.sections():
        env = {'name': section}
        env.update(config[section])
        environments.append(env)
    return render_template('environments.html', environments=environments)

if __name__ == '__main__':
    app.run(debug=True)
