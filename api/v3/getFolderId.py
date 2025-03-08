import json

import requests
from flask import session
import binascii
import datetime
import json
import logging
import os
import random
import string
import time
from logging.handlers import TimedRotatingFileHandler
from urllib.parse import quote, urlencode

from router import app

# 配置日志
log_dir = "logs"
log_file = f"{log_dir}/crawler_{datetime.datetime.now().strftime('%Y-%m-%d')}.log"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

file_handler = TimedRotatingFileHandler(
    log_file,
    when="midnight",
    interval=1,
    encoding='utf-8'
)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)

logger = logging.getLogger('crawler')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


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
            'devType': 6,
            'devModel': 'Chrome',
            'uuid': 'HGFdZF5RJGv61cyMiY7S2',
            'shareId': shareId,
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
        logger.info(f"{response.url}")
        logger.info(f"{response.text}")
        # print(response.url)
        # print(response.text)
        if response.status_code == 200:
            LISTS = json.loads(response.text)
            data = {"code": 200, "status": "获取成功", "folders": LISTS['list']}
            return data
        else:
            return {"code": 400, "status": "获取失败", "folders": None}
    except Exception as e:
        return str(e)
