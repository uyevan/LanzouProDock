import json

import requests
from flask import session

from router import app


@app.route('/v3/iGetFolderId/<shareId>/<int:Page>/<int:Limit>', methods=["GET"])
def iGetFolderId(shareId, Page, Limit):
    session.permanent = True
    try:
        if shareId == '':
            return {"code": 400, "status": "shareId不能为空", "folders": None}
        if Page == '' or Limit == '':
            Page = 1
            Limit = 30
        rUrl = 'https://api.ilanzou.com/unproved/recommend/list'
        rParams = {
            'shareId': shareId,
            'offset': Page,
            'limit': Limit
        }
        # 获取列表数据并返回
        response = requests.get(url=rUrl, params=rParams)
        if response.status_code == 200:
            LISTS = json.loads(response.text)
            data = {"code": 200, "status": "获取成功", "folders": LISTS['list']}
            return data
        else:
            return {"code": 400, "status": "获取失败", "folders": None}
    except Exception as e:
        return str(e)
