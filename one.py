from flask import Flask
from flask import jsonify
from lxml import etree
from flask import request
import requests

app = Flask(__name__)


@app.route('/get_folder_data')
def get_folder_data():
    try:
        # 获取传入的 URL
        url = request.args.get('url')
        print(url)
        # 使用你的原始代码获取文件夹数据
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 HBPC/12.1.2.300"
        NAME = []
        URL = []

        with requests.get(url, headers={'User-agent': ua}) as res:
            content = res.text
            html = etree.HTML(content)

            # 获取文件夹名
            name = html.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "filename", " " ))]/text()')
            NAME.extend(name)

            # 获取文件夹链接
            url = html.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mlink minPx-top", " " ))]/@href')
            URL.extend(url)

        json_data = []
        for i in range(len(NAME)):
            json_obj = {
                "id": i + 1,
                "name": NAME[i],
                "url": f"https://www.lanzoux.com{URL[i]}"
            }
            json_data.append(json_obj)

        print(json_data)
        return jsonify(json_data)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3307)
