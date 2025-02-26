import json

import requests
from flask import session

from router import app


@app.route('/v3/iGetFiles/<shareId>/<int:folderId>/<int:Page>/<int:Limit>', methods=["GET"])
def iGetFiles(shareId, folderId, Page, Limit):
    session.permanent = True
    try:
        if shareId == '' or folderId == '':
            return {"code": 400, "status": "shareId/folderId不能为空", "files": None}
        if Page == '' or Limit == '':
            Page = 1
            Limit = 30
        rUrl = 'https://api.ilanzou.com/unproved/share/list'
        rParams = {
            'devType': 3,
            'devModel': 'Chrome',
            'uuid': 'HGFdZF5RJGv61cyMiY7S2',
            'shareId': shareId,
            'folderId': folderId,
            'offset': Page,
            'limit': Limit
        }
        # 添加请求头
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'api.ilanzou.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-gpc': '1'
        }
        # 获取列表数据并返回
        response = requests.get(url=rUrl, params=rParams, headers=headers)  # 添加 headers 参数
        if response.status_code == 200:
            LISTS = json.loads(response.text)
            data = {"code": 200, "status": "获取成功", "files": LISTS['list']}
            return data
        else:
            return {"code": 400, "status": "获取失败", "files": None}
    except Exception as e:
        return str(e)
