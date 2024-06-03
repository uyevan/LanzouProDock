import flask
import requests

from router import app


@app.route('/v1/parseById', methods=["GET"])
def parseById():
    Fid = flask.request.values.get("id")
    dowUrl = f'https://lanzou.fyaa.net/lanzou/?url=https://www.lanzoux.com/{Fid}&type=down'
    response = requests.get(url=dowUrl, allow_redirects=False)
    data = {"code": 200, "status": "解析成功", "url": response.next.url}
    return data
