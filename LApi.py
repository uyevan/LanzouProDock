import json
import re
import secrets
from datetime import timedelta

import flask
import requests
from flask import Flask, session
from gevent import pywsgi
from lxml import etree

app = Flask(__name__)
# app.secret_key = secrets.token_hex(16) 等同于下面一行
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)  # 配置7天有效


# noinspection DuplicatedCode
@app.route('/getAll', methods=["GET"])
def getAll():
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
            foldersName = html.xpath('//*[@id="folder"]/div[*]/a/div[2]/text()')
            foldersDes = html.xpath('//*[@id="folder"]/div[*]/a/div[2]/div[1]/text()')
            foldersUrl = html.xpath('//*[@id="folder"]/div[*]/a/@href')
            FOLDERS = []  # 存储文件夹信息
            for folder in range(len(foldersUrl)):
                folderJson = {
                    "name": foldersName[folder],
                    "description": foldersDes[folder],
                    "url": foldersUrl[folder]
                }
                FOLDERS.append(folderJson)

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
            print('会话中存在：', url_match, '|', file_match, '|', t_match, '|', k_match)
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
                print('会话中不存在：', url_match, '|', file_match, '|', t_match, '|', k_match)

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


@app.route('/getFolders', methods=["GET"])
def getFolders():
    try:
        url = flask.request.values.get("url")
        if url == '':
            return {"code": 400, "status": "Url链接不能为空", "folders": None}
        # 使用你的原始代码获取文件夹数据
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 HBPC/12.1.2.300"
        with requests.get(url, headers={'User-agent': ua}) as res:
            content = res.text
            html = etree.HTML(content)

            # 获取文件夹
            foldersName = html.xpath('//*[@id="folder"]/div[*]/a/div[2]/text()')
            foldersDes = html.xpath('//*[@id="folder"]/div[*]/a/div[2]/div[1]/text()')
            foldersUrl = html.xpath('//*[@id="folder"]/div[*]/a/@href')
            FOLDERS = []  # 存储文件夹信息
            for folder in range(len(foldersUrl)):
                if folder < len(foldersDes):
                    description = foldersDes[folder]
                else:
                    description = '暂无简介呀~'
                folderJson = {
                    "name": foldersName[folder],
                    "description": description,
                    "url": foldersUrl[folder]
                }
                FOLDERS.append(folderJson)

            data = {"code": 200, "status": "获取成功", "folders": FOLDERS}
            '''js = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
            print(js)'''
            return data
    except Exception as e:
        return str(e)


# noinspection DuplicatedCode
@app.route('/getFiles', methods=["GET"])
def getFiles():
    try:
        url = flask.request.values.get("url")
        page = flask.request.values.get("page")
        if url == '':
            return {"code": 400, "status": "Url链接不能为空", "files": None}
        if page == '':
            page = 1
        # 使用你的原始代码获取文件夹数据
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

            url_match = session.get('url_match')
            file_match = session.get('file_match')
            t_match = session.get('t_match')
            k_match = session.get('k_match')
            print('会话中存在：', url_match, '|', file_match, '|', t_match, '|', k_match)

            # 如果参数不存在于会话中，则从请求中获取它们
            if not url_match or not file_match or not t_match or not k_match:
                url_match = re.search(r"url\s*:\s*'(/filemoreajax\.php\?file=\d+)'", content).group(1)  # 截取请求地址
                file_match = re.search(r"\d+", url_match).group()  # fid
                t_match = re.search(r"var\s+i\w+\s*=\s*'([^']*)';", content).group(1)  # 时间戳
                k_match = re.search(r"var\s+_\w+\s*=\s*'([^']*)';", content).group(1)  # 签名
                # 将参数存储到会话中，以便后续请求可以使用它们
                session['url_match'] = url_match
                session['file_match'] = file_match
                session['t_match'] = t_match
                session['k_match'] = k_match
                print('会话中不存在：', url_match, '|', file_match, '|', t_match, '|', k_match)

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
            data = {"code": 200, "status": "获取成功", "files": FILES}
            '''js = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
            print(js)'''
            return data
    except Exception as e:
        return str(e)


@app.route('/search', methods=["GET"])
def search():
    try:
        url = flask.request.values.get("url")
        wd = flask.request.values.get("wd")
        if url == '':
            return {"code": 400, "status": "Url链接不能为空", "files": None}
        if wd == '':
            return {"code": 400, "status": "关键词链接不能为空", "files": None}
        # 使用你的原始代码获取文件夹数据
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
                "wd": f"{wd}",
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


@app.route('/downloadByUrl', methods=["GET"])
def downloadByUrl():
    url = flask.request.values.get("url")
    dowUrl = f'https://lanzou.fyaa.net/lanzou/?url={url}&type=down'
    response = requests.get(url=dowUrl, allow_redirects=False)
    data = {"code": 200, "status": "解析成功", "url": response.next.url}
    return data


@app.route('/downloadById', methods=["GET"])
def downloadById():
    Fid = flask.request.values.get("id")
    dowUrl = f'https://lanzou.fyaa.net/lanzou/?url=https://www.lanzoux.com/{Fid}&type=down'
    response = requests.get(url=dowUrl, allow_redirects=False)
    data = {"code": 200, "status": "解析成功", "url": response.next.url}
    return data


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=3307)
    server = pywsgi.WSGIServer(('0.0.0.0', 3307), app)
    server.serve_forever()
