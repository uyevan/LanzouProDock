import flask
import requests
from lxml import etree

from router import app


@app.route('/v1/getDirectory', methods=["GET"])
def getDirectory():
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
