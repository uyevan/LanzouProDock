import requests

from router import app


@app.route('/v2/parseByUrl/<path:Url>', methods=["GET", "POST"])
def parseByUrlV2(Url):
    print(Url)
    dowUrl = f'https://lanzou.fyaa.net/lanzou/?url={Url}&type=down'
    response = requests.get(url=dowUrl, allow_redirects=False)
    data = {"code": 200, "status": "解析成功", "url": response.next.url}
    return data
