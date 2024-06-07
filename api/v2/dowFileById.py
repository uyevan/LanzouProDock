from flask import session

from api.lib.DownLoadLib import get_final_download_link
from router import app


@app.route('/v2/parseById/<Type>/<Fid>', methods=["GET", "POST"])
def parseByIdV2(Type, Fid):
    session.permanent = True
    # @外部解析接口
    # dowUrl = f'https://lanzou.fyaa.net/lanzou/?url=https://www.lanzoux.com/{Fid}&type=down'
    # response = requests.get(url=dowUrl, allow_redirects=False)
    # data = {"code": 200, "status": "解析成功", "url": response.next.url}
    # @内部接口访问
    dowUrl = f'https://www.lanzoux.com/{Fid}'
    response = get_final_download_link(dowUrl, Type)
    data = {"code": 200, "status": "解析成功", "url": response}
    return data
