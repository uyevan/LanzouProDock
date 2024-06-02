import flask
import requests
from flask import Flask

app = Flask(__name__)


@app.route('/downloadByUrl', methods=["GET"])
def downloadByUrl():
    url = flask.request.values.get("url")
    dowUrl = f'https://lanzou.fyaa.net/lanzou/?url={url}&type=down'
    response = requests.get(url=dowUrl, allow_redirects=False)
    data = {"code": 200, "status": "解析成功", "url": response.next.url}
    return data


@app.route('/downloadById', methods=["GET"])
def downloadById():
    Fid = flask.request.values.get("id")
    dowUrl = f'https://lanzou.fyaa.net/lanzou/?url=https://www.lanzoux.com/{Fid}&type=down'
    response = requests.get(url=dowUrl, allow_redirects=False)
    data = {"code": 200, "status": "解析成功", "url": response.next.url}
    return data
