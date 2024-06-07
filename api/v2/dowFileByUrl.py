from api.lib.DownLoadLib import get_final_download_link
from router import app


@app.route('/v2/parseByUrl/<Type>/<path:Url>', methods=["GET", "POST"])
def parseByUrlV2(Type, Url):
    # @外部接口解析
    # dowUrl = f'https://lanzou.fyaa.net/lanzou/?url={Url}&type=down'
    # response = requests.get(url=dowUrl, allow_redirects=False)
    # data = {"code": 200, "status": "解析成功", "url": response.next.url}
    # @内部接口解析
    dowUrl = Url
    response = get_final_download_link(dowUrl, Type)
    data = {"code": 200, "status": "解析成功", "url": response}
    return data
