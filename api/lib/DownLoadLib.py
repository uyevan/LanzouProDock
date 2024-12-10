import json
import re
import time
import requests
from functools import lru_cache

# 全局常量定义
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
}

DOWNLOAD_HEADERS = {
    **DEFAULT_HEADERS,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
    "sec-fetch-dest": "document",
    "cookie": "down_ip=1"
}

def retry_request(func):
    """自定义重试装饰器"""
    def wrapper(*args, **kwargs):
        max_retries = 3
        retry_delay = 0.1
        last_exception = None

        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except requests.RequestException as e:
                last_exception = e
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # 指数退避
                continue
        raise last_exception
    return wrapper

@lru_cache(maxsize=128)
def re_domain(url):
    match = re.match(r"https?://([^/]+)", url)
    return match.group(1) if match else None

@retry_request
def safe_request(method, url, **kwargs):
    """统一的请求处理函数"""
    try:
        kwargs.setdefault('timeout', (5, 15))
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"请求失败: {str(e)}")

def extract_link(response_text, pattern):
    try:
        return re.search(pattern, response_text).group(1)
    except (AttributeError, IndexError):
        return None

def getPFile(url, password):
    """优化的带密码文件处理函数"""
    domain = re_domain(url)
    if not domain:
        raise ValueError("无效的URL")

    response = safe_request('GET', url, headers=DEFAULT_HEADERS)
    text = response.text

    url_match = re.search(r"url\s*:\s*'(/ajaxm\.php\?file=\d+)'", text)
    skewbalds_match = re.search(r"var\s+skdklds\s*=\s*'([^']*)';", text)

    if not all([url_match, skewbalds_match]):
        raise ValueError("无法提取必要信息")

    data = {
        'action': 'downprocess',
        'sign': skewbalds_match.group(1),
        'p': password,
    }

    headers = {**DEFAULT_HEADERS, 'Referer': url}
    response = safe_request('POST',
                            f"https://{domain}{url_match.group(1)}",
                            headers=headers,
                            data=data)

    try:
        json_data = response.json()
        full_url = f"{json_data['dom']}/file/{json_data['url']}"
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"解析响应失败: {str(e)}")

    response = safe_request('GET', full_url,
                            headers=DOWNLOAD_HEADERS,
                            allow_redirects=False)

    return response.headers.get('Location')

def getDPFile(url, fType):
    """优化的普通文件处理函数"""
    if fType not in {'new', 'old'}:
        raise ValueError('Type类型错误')

    domain = re_domain(url)
    if not domain:
        raise ValueError("无效的URL")

    patterns = {
        'new': (r'<iframe\s+class="n_downlink"\s+name="\d+"\s+src="([^"]+)"', 0),
        'old': (r'<iframe\s+class="ifr2"\s+name="\d+"\s+src="([^"]+)"', 1)
    }
    pattern, math_num = patterns[fType]

    response = safe_request('GET', url, headers=DEFAULT_HEADERS)
    matches = re.findall(pattern, response.text)
    if not matches or len(matches) <= math_num:
        raise ValueError("无法找到下载框架")

    iframe_url = f"https://{domain}{matches[math_num]}"
    response = safe_request('GET', iframe_url, headers=DEFAULT_HEADERS)

    sign = extract_link(response.text, r"'sign'\s*:\s*'([^']+)'")
    url2 = extract_link(response.text, r"url\s*:\s*'([^']+)'")

    if not all([sign, url2]):
        raise ValueError("无法提取签名信息")

    data = {
        'action': 'downprocess',
        'signs': '?ctdf',
        'sign': sign,
        'websign': '',
        'websignkey': 'bL27',
        'ves': 1
    }

    headers = {**DEFAULT_HEADERS, 'Referer': matches[math_num]}
    response = safe_request('POST',
                            f"https://{domain}{url2}",
                            headers=headers,
                            data=data)

    try:
        json_data = response.json()
        full_url = f"{json_data['dom']}/file/{json_data['url']}"
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"解析响应失败: {str(e)}")

    response = safe_request('GET', full_url,
                            headers=DOWNLOAD_HEADERS,
                            allow_redirects=False)

    return response.headers.get('Location')

def get_final_download_link(url, Type='new', pwd=''):
    """主函数优化"""
    if not url or not Type:
        return '参数不能为空'

    try:
        response = safe_request('GET', url, headers=DEFAULT_HEADERS)
        text = response.text

        if not pwd and "<title>文件</title>" in text:
            return '此文件需要密码'
        if "文件取消分享了" in text:
            return '来晚啦...文件取消分享了'

        # 根据是否有密码选择处理函数
        handler = getPFile if pwd else getDPFile
        result = handler(url, pwd if pwd else Type)
        return result or '获取下载链接失败'

    except Exception as e:
        return f'处理失败: {str(e)}'