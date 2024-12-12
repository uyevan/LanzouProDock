import binascii
import random
import string
import time
import logging
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from router import app

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/v3/iParse/<int:fileId>', methods=["GET"])
def iParse(fileId):
    logger.info(f"Starting to process file ID: {fileId}")

    try:
        rUrl = 'https://api.ilanzou.com/unproved/file/redirect'
        rTime = str(int(round(time.time() * 1000)))

        # Build request parameters
        rParams = {
            "downloadId": aes_ecb_pkcs7_encrypt(f"{fileId}|", 'lanZouY-disk-app'),
            "enable": 1,
            "devType": 3,
            "uuid": generate_random_string(21),
            "timestamp": aes_ecb_pkcs7_encrypt(rTime, 'lanZouY-disk-app'),
            "auth": aes_ecb_pkcs7_encrypt(f"{fileId}|{rTime}", 'lanZouY-disk-app')
        }

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

        logger.info(f"Request URL: {rUrl}")
        logger.info(f"Request parameters: {rParams}")
        logger.info(f"Request headers: {headers}")



        response = requests.get(
            url=rUrl,
            params=rParams,
            headers=headers,
            allow_redirects=False,
            timeout=10
        )

        print("请求地址:"+response.url)

        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response content: {response.text}")

        if response.status_code in (200, 302):
            try:
                if response.status_code == 302:
                    redirect_url = response.headers.get('Location')
                    logger.info(f"Parse successful, redirect URL: {redirect_url}")
                    return {"code": 200, "status": "Parse successful", "url": redirect_url}
                else:
                    # Handle 200 status code JSON response
                    json_response = response.json()
                    logger.info(f"JSON response: {json_response}")
                    if 'url' in json_response:
                        return {"code": 200, "status": "Parse successful", "url": json_response['url']}
                    elif 'data' in json_response and isinstance(json_response['data'], dict):
                        if 'url' in json_response['data']:
                            return {"code": 200, "status": "Parse successful", "url": json_response['data']['url']}
            except Exception as e:
                logger.error(f"Error processing response: {str(e)}", exc_info=True)

        logger.warning(f"Parse failed, status code: {response.status_code}, response content: {response.text}")
        return {"code": 400, "status": "Parse failed", "url": None}

    except Exception as e:
        logger.error(f"Processing exception: {str(e)}", exc_info=True)
        return {"code": 500, "status": f"Server error: {str(e)}", "url": None}

# AES encryption
def aes_ecb_pkcs7_encrypt(plaintext, key):
    key_bytes = key.encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_plaintext)
    encrypted_hex = binascii.hexlify(encrypted_bytes).decode('utf-8')
    logger.debug(f"AES encryption result: {encrypted_hex}")
    return encrypted_hex.upper()

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    random_str = ''.join(random.choice(letters) for _ in range(length))
    logger.debug(f"Generated random string: {random_str}")
    return random_str