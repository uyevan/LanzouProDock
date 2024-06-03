import requests

from router import app


@app.route('/v2/parseById/<Fid>', methods=["GET", "POST"])
def parseByIdV2(Fid):
    dowUrl = f'https://lanzou.fyaa.net/lanzou/?url=https://www.lanzoux.com/{Fid}&type=down'
    response = requests.get(url=dowUrl, allow_redirects=False)
    data = {"code": 200, "status": "解析成功", "url": response.next.url}
    return data
