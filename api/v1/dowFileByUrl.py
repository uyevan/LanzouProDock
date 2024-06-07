import flask

from api.lib.DownLoadLib import get_final_download_link
from router import app


@app.route('/v1/parseByUrl', methods=["GET"])
def parseByUrl():
    url = flask.request.values.get("url")
    Type = flask.request.values.get("type")
    # @外部接口范文
    # dowUrl = f'https://lanzou.fyaa.net/lanzou/?url={url}&type=down'
    # response = requests.get(url=dowUrl, allow_redirects=False)
    # data = {"code": 200, "status": "解析成功", "url": response.next.url}
    # @内部接口访问
    dowUrl = url
    response = get_final_download_link(dowUrl, Type)
    data = {"code": 200, "status": "解析成功", "url": response}
    return data
