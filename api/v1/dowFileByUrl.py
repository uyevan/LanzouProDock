import flask
import requests

from router import app


@app.route('/v1/parseByUrl', methods=["GET"])
def parseByUrl():
    url = flask.request.values.get("url")
    dowUrl = f'https://lanzou.fyaa.net/lanzou/?url={url}&type=down'
    response = requests.get(url=dowUrl, allow_redirects=False)
    data = {"code": 200, "status": "解析成功", "url": response.next.url}
    return data
