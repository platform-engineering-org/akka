from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    """Function printing Hello, World!"""
    return "Hello, World!"
