import flask
from flask import session

from api.lib.DownLoadLib import get_final_download_link
from router import app


@app.route('/v1/parseById', methods=["GET"])
def parseById():
    session.permanent = True
    Fid = flask.request.values.get("id")
    Type = flask.request.values.get("type")
    Pwd = flask.request.values.get("pwd")
    if Pwd is None or Pwd == "":
        Pwd = ""
    # @调用外部接口
    # dowUrl = f'https://lanzou.fyaa.net/lanzou/?url=https://www.lanzoux.com/{Fid}&type=down'
    # response = requests.get(url=dowUrl, allow_redirects=False)
    # data = {"code": 200, "status": "解析成功", "url": response.next.url}
    # @内部解析方法
    dowUrl = f'https://www.lanzoux.com/{Fid}'
    response = get_final_download_link(dowUrl, Type, Pwd)
    data = {"code": 200, "status": "解析成功", "url": response}
    return data
