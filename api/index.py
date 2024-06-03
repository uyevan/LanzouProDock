from flask import render_template

from router import app


@app.route('/', methods=['GET'])
def indexA():
    return render_template("index.html")


@app.route('/index', methods=['GET'])
def indexB():
    return render_template("index.html")
