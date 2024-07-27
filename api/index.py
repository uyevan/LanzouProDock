from flask import render_template

from router import app


@app.route('/', methods=['GET'])
def indexA():
    return render_template("index.html")


@app.route('/index', methods=['GET'])
def indexB():
    return render_template("index.html")


@app.route('/api-dock-v1.html', methods=['GET'])
def indexC():
    return render_template('api-dock-v1.html')


@app.route('/api-dock-v2.html', methods=['GET'])
def indexD():
    return render_template('api-dock-v2.html')


@app.route('/api-dock-v3.html', methods=['GET'])
def indexE():
    return render_template('api-dock-v3.html')


@app.route('/api-about.html', methods=['GET'])
def indexF():
    return render_template('api-about.html')


@app.route('/404.html', methods=['GET'])
def index404():
    return render_template('404.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500
