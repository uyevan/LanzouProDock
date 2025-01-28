import json

import requests
from flask import session

from router import app


@app.route('/v3/iSearchFile/<shareId>/<int:folderId>/<Wd>/<int:Page>/<int:Limit>', methods=["GET"])
def iSearchFile(shareId, folderId, Wd, Page, Limit):
    session.permanent = True
    try:
        if shareId == '' or folderId == '' or Wd == '':
            return {"code": 400, "status": "shareId/folderId/Wd不能为空", "files": None}
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
            'limit': Limit,
            'search': Wd
        }
        # 获取列表数据并返回
        response = requests.get(url=rUrl, params=rParams)
        if response.status_code == 200:
            LISTS = json.loads(response.text)
            data = {"code": 200, "status": "获取成功", "files": LISTS['list']}
            return data
        else:
            return {"code": 400, "status": "获取失败", "files": None}
    except Exception as e:
        return str(e)
