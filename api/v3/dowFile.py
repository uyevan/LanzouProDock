import binascii
import random
import string
import time
import logging
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from flask import session as flask_session
from router import app

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/v3/iParse/<int:fileId>', methods=["GET"])
def iParse(fileId):
    flask_session.permanent = True  # 使用重命名后的flask_session
    logger.info(f"开始处理文件ID: {fileId}")

    try:
        rUrl = 'https://api.ilanzou.com/unproved/file/redirect'
        rTime = str(int(round(time.time() * 1000)))

        # 构建请求参数
        rParams = {
            "downloadId": aes_ecb_pkcs7_encrypt(f"{fileId}|", 'lanZouY-disk-app'),
            "enable": 1,
            "devType": 3,
            "uuid": str(generate_random_string(21)),
            "timestamp": aes_ecb_pkcs7_encrypt(rTime, 'lanZouY-disk-app'),
            "auth": aes_ecb_pkcs7_encrypt(f"{fileId}|{rTime}", 'lanZouY-disk-app')
        }

        # 添加完整的请求头，包括 CORS 相关的头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://www.ilanzou.com',
            'Referer': 'https://www.ilanzou.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Connection': 'keep-alive',
            'Cookie': 'down_ip=1'
        }

        # 创建requests的session并重命名为req_session
        with requests.Session() as req_session:
            req_session.headers.update(headers)
            response = req_session.get(
                url=rUrl,
                params=rParams,
                allow_redirects=False,
                timeout=10
            )

            if response.status_code in (200, 302):
                try:
                    if response.status_code == 302:
                        redirect_url = response.headers['Location']
                        return {"code": 200, "status": "解析成功", "url": redirect_url}
                    else:
                        # 处理 200 状态码的JSON响应
                        json_response = response.json()
                        if 'url' in json_response:
                            return {"code": 200, "status": "解析成功", "url": json_response['url']}
                        elif 'data' in json_response and isinstance(json_response['data'], dict):
                            if 'url' in json_response['data']:
                                return {"code": 200, "status": "解析成功", "url": json_response['data']['url']}
                except Exception as e:
                    logger.error(f"处理响应时出错: {str(e)}", exc_info=True)

            return {"code": 400, "status": "解析失败", "url": None}

    except Exception as e:
        logger.error(f"处理异常: {str(e)}", exc_info=True)
        return {"code": 500, "status": f"服务器异常: {str(e)}", "url": None}

# AES加密
def aes_ecb_pkcs7_encrypt(plaintext, key):
    # 将密钥转换为字节串
    key_bytes = key.encode('utf-8')
    # 创建AES加密器，使用ECB模式
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    # 对明文进行PKCS7填充
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    # 加密并返回十六进制结果
    encrypted_bytes = cipher.encrypt(padded_plaintext)
    encrypted_hex = binascii.hexlify(encrypted_bytes).decode('utf-8')
    return encrypted_hex.upper()


def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
