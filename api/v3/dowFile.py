import binascii
import random
import string
import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from flask import session

from router import app


@app.route('/v3/iParse/<int:fileId>', methods=["GET"])
def iParse(fileId):
    session.permanent = True
    try:
        if fileId == '':
            return {"code": 400, "status": "fileId不能为空", "url": None}
        rUrl = 'https://api.ilanzou.com/unproved/file/redirect'
        rTime = str(int(round(time.time() * 1000)))
        rParams = {
            "downloadId": aes_ecb_pkcs7_encrypt(f"{fileId}|", 'lanZouY-disk-app'),
            "enable": 1,
            "devType": 3,
            "uuid": str(generate_random_string(21)),
            "timestamp": aes_ecb_pkcs7_encrypt(rTime, 'lanZouY-disk-app'),
            "auth": aes_ecb_pkcs7_encrypt(f"{fileId}|{rTime}", 'lanZouY-disk-app')
        }
        # 获取列表数据并返回
        response = requests.get(url=rUrl, params=rParams, allow_redirects=False)
        if response.status_code == 302:
            redirect_url = response.headers['Location']
            data = {"code": 200, "status": "解析成功", "url": redirect_url}
            return data
        else:
            return {"code": 400, "status": "解析失败", "url": None}
    except Exception as e:
        return str(e)


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
