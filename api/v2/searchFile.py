import json
import re

import requests
from flask import session

from router import app


@app.route('/v2/searchFile/<Lid>/<Wd>', methods=["GET"])
def searchFileV2(Lid, Wd):
    session.permanent = True
    try:
        if Lid == '':
            return {"code": 400, "status": "Lid不能为空", "files": None}
        if Wd == '':
            return {"code": 400, "status": "关键词链接不能为空", "files": None}
        # 使用你的原始代码获取文件夹数据
        url = f'https://www.lanzoux.com/{Lid}'
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 HBPC/12.1.2.300"
        with requests.get(url, headers={'User-agent': ua}) as res:
            content = res.text
            # html = etree.HTML(content)  # 解析成html对象
            # 获取文件
            requestsSession = requests.Session()
            requestsSession.headers.update({
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36 Edg/122.0.0.0",
                "authority": "www.lanzoux.com",
                "accept": "application/json, text/javascript, */*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "cache-control": "no-cache",
                "dnt": "1",
                "origin": "https://www.lanzoux.com",
                "pragma": "no-cache",
                "referer": f"{url}",
                "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand)\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": "\"Android\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest"
            })

            cookies = {
                "codelen": "1"
            }
            requestsSession.cookies.update(cookies)
            # 尝试从会话中获取参数
            sign = re.search(r"'sign'\s*:\s*'([^']+)'", content).group(1)  # 签名
            url = f"https://www.lanzoux.com" + "/search/s.php"
            data = {
                "wd": f"{Wd}",
                "sign": f"{sign}",
            }
            response = requestsSession.post(url, data=data,
                                            headers={"Content-Type": "application/x-www-form-urlencoded"})
            FILES = json.loads(response.text)
            data = {"code": 200, "status": "获取成功", "files": FILES}
            '''js = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
            print(js)'''
            return data
    except Exception as e:
        return str(e)
