#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

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


def aes_ecb_pkcs7_encrypt(plaintext, key):
    """
    AES ECB模式加密函数，增强了编码处理
    """
    try:
        # 强制转换输入为utf-8字节串
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8').decode('utf-8').encode('utf-8')
        if isinstance(key, str):
            key = key.encode('utf-8').decode('utf-8').encode('utf-8')

        # 确保密钥长度为16字节
        key = key.ljust(16, b'\0')[:16]

        logger.info(f"开始加密数据,密钥长度:{len(key)}")

        # 使用ECB模式创建cipher对象
        cipher = AES.new(key, AES.MODE_ECB)

        # 确保明文是字节类型并进行PKCS7填充
        if not isinstance(plaintext, bytes):
            plaintext = plaintext.encode('utf-8')
        padded_data = pad(plaintext, AES.block_size)

        # 加密并转换为大写十六进制
        encrypted_bytes = cipher.encrypt(padded_data)
        result = binascii.hexlify(encrypted_bytes).decode('utf-8').upper()

        logger.info("加密成功")
        return result
    except Exception as e:
        logger.error(f"加密失败: {str(e)}, 明文: {plaintext}, 密钥: {key}")
        raise


def generate_random_string(length):
    """生成指定长度的随机字符串"""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


@app.route('/v3/iParse/<int:fileId>', methods=["GET"])
def iParse(fileId):
    """处理文件解析请求的接口"""
    try:
        logger.info(f"接收到文件解析请求,文件ID:{fileId}")

        rUrl = 'https://api.ilanzou.com/unproved/file/redirect'

        # 确保时间戳字符串的正确编码
        rTime = str(int(round(time.time() * 1000)))
        rTime = rTime.encode('utf-8').decode('utf-8')

        # 使用显式命名的字典键构建参数并进行URL编码
        rParams = {
            str('downloadId'): quote(aes_ecb_pkcs7_encrypt(f"{fileId}|", 'lanZouY-disk-app')),
            str('enable'): 1,
            str('devType'): 6,
            str('uuid'): quote(generate_random_string(21)),
            str('timestamp'): quote(aes_ecb_pkcs7_encrypt(rTime, 'lanZouY-disk-app')),
            str('auth'): quote(aes_ecb_pkcs7_encrypt(f"{fileId}|{rTime}", 'lanZouY-disk-app')),
            str("shareId"): generate_random_string(8)
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

        logger.info("开始发送请求...")
        # 发送请求
        response = requests.get(
            url=rUrl,
            headers=headers,
            params=rParams,
            allow_redirects=False,
            timeout=10
        )

        # 记录请求和响应信息
        logger.info(f"请求URL: {response.url}")
        logger.info(f"请求参数: {json.dumps(rParams, ensure_ascii=False)}")
        logger.info(f"请求头: {json.dumps(dict(response.request.headers), ensure_ascii=False)}")
        logger.info(f"响应状态码: {response.status_code}")
        logger.info(f"响应头: {json.dumps(dict(response.headers), ensure_ascii=False)}")

        try:
            response_text = response.text
            logger.info(f"响应内容: {response_text}")
        except Exception as e:
            logger.warning(f"响应内容解码失败: {str(e)}")

        # 处理响应
        if response.status_code in (200, 302):
            try:
                if response.status_code == 302:
                    redirect_url = response.headers.get('Location')
                    logger.info(f"解析成功,获取重定向地址:{redirect_url}")
                    return {"code": 200, "status": "Parse successful", "url": redirect_url}
                else:
                    # 处理JSON响应
                    json_response = response.json()
                    if 'url' in json_response:
                        logger.info("解析成功,获取直接URL")
                        return {"code": 200, "status": "Parse successful", "url": json_response['url']}
                    elif 'data' in json_response and isinstance(json_response['data'], dict):
                        if 'url' in json_response['data']:
                            logger.info("解析成功,获取嵌套URL")
                            return {"code": 200, "status": "Parse successful", "url": json_response['data']['url']}
            except Exception as e:
                logger.error(f"响应处理失败:{str(e)}")

        logger.warning(f"解析失败,状态码:{response.status_code}")
        return {"code": 400, "status": "Parse failed", "url": None}

    except Exception as e:
        logger.error(f"请求出错:{str(e)}")
        return {"code": 500, "status": f"Server error: {str(e)}", "url": None}


@app.route('/v3/iParse301/<int:fileId>', methods=["GET"])
def iParse301(fileId):
    """构建文件解析URL的接口"""
    try:
        logger.info(f"接收到URL构建请求,文件ID:{fileId}")

        base_url = 'https://api.ilanzou.com/unproved/file/redirect'

        # 生成时间戳
        rTime = str(int(round(time.time() * 1000)))
        rTime = rTime.encode('utf-8').decode('utf-8')

        # 构建参数字典
        params = {
            'downloadId': aes_ecb_pkcs7_encrypt(f"{fileId}|", 'lanZouY-disk-app'),
            'enable': 1,
            'devType': 6,
            'uuid': generate_random_string(21),
            'timestamp': aes_ecb_pkcs7_encrypt(rTime, 'lanZouY-disk-app'),
            'auth': aes_ecb_pkcs7_encrypt(f"{fileId}|{rTime}", 'lanZouY-disk-app'),
            'shareId': generate_random_string(8)
        }

        # 构建完整URL
        full_url = f"{base_url}?{urlencode(params)}"

        logger.info(f"URL构建成功: {full_url}")

        return {
            "code": 200,
            "status": "URL generated successfully",
            "url": full_url
        }

    except Exception as e:
        logger.error(f"URL构建失败:{str(e)}")
        return {
            "code": 500,
            "status": f"URL generation failed: {str(e)}",
            "url": None
        }
