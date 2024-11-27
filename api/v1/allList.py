import json
import re

import flask
import requests
from flask import session
from lxml import etree

from router import app


# noinspection DuplicatedCode
@app.route('/v1/getFilesAndDirectories', methods=["GET"])
def getFilesAndDirectories():
    session.permanent = True
    try:
        url = flask.request.values.get("url")
        page = flask.request.values.get("page")
        if url == '':
            return {"code": 400, "status": "Url链接不能为空", "folders": None, "files": None}
        if page == '':
            page = 1
        # 使用你的原始代码获取文件夹数据
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 HBPC/12.1.2.300"
        with requests.get(url, headers={'User-agent': ua}) as res:
            content = res.text
            html = etree.HTML(content)  # 解析成html对象

            # 获取文件夹
            # 获取文件夹,增加错误处理
            FOLDERS = []
            try:
                folders_elements = html.xpath('//*[@id="folder"]/div')
                for folder in folders_elements:
                    name = folder.xpath('.//a/div[2]/text()')
                    description = folder.xpath('.//a/div[2]/div[1]/text()')
                    url = folder.xpath('.//a/@href')

                    if name and url:
                        folderJson = {
                            "name": name[0],
                            "description": description[0] if description else "",
                            "url": url[0]
                        }
                        FOLDERS.append(folderJson)
            except Exception as e:
                print(f"获取文件夹信息出错: {str(e)}")

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

            url_match = session.get('url_match')
            file_match = session.get('file_match')
            t_match = session.get('t_match')
            k_match = session.get('k_match')
            # print('会话中存在：', url_match, '|', file_match, '|', t_match, '|', k_match)
            # 如果参数不存在于会话中，则从请求中获取它们
            if not url_match or not file_match or not t_match or not k_match or url_match is None or file_match is None or t_match is None or k_match is None:
                url_match = re.search(r"url\s*:\s*'(/filemoreajax\.php\?file=\d+)'", content).group(1)  # 截取请求地址
                file_match = re.search(r"\d+", url_match).group()  # fid
                t_match = re.search(r"var\s+i\w+\s*=\s*'([^']*)';", content).group(1)  # 时间戳
                k_match = re.search(r"var\s+_\w+\s*=\s*'([^']*)';", content).group(1)  # 签名
                # 将参数存储到会话中，以便后续请求可以使用它们
                session['url_match'] = url_match
                session['file_match'] = file_match
                session['t_match'] = t_match
                session['k_match'] = k_match
                # print('会话中不存在：', url_match, '|', file_match, '|', t_match, '|', k_match)

            url = f"https://www.lanzoux.com" + url_match
            data = {
                "lx": "2",
                "fid": file_match,
                "uid": "941967",
                "pg": f"{page}",
                "rep": "0",
                "t": t_match,
                "k": k_match,
                "up": "1",
                "vip": "0",
                "webfoldersign": ""
            }

            response = requestsSession.post(url, data=data,
                                            headers={"Content-Type": "application/x-www-form-urlencoded"})
            FILES = json.loads(response.text)
            data = {"code": 200, "status": "获取成功", "folders": FOLDERS, "files": FILES}
            '''js = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
            print(js)'''
            return data
    except Exception as e:
        return str(e)
