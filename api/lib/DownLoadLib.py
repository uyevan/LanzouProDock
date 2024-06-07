import json
import re

import requests


def get_final_download_link(url, type='new'):
    def re_domain(Lurl):
        pattern_domain = r"https?://([^/]+)"
        match = re.search(pattern_domain, Lurl)
        if match:
            doMain = match.group(1)
            return doMain
        else:
            return None

    def extract_link(response_text, pattern):
        match = re.search(pattern, response_text)
        if match:
            return match.group(1)
        else:
            return None

    if url == '' or type == '':
        return '参数不能为空'
    if type not in {'new', 'old'}:
        return 'Type类型错误'
    doMain = re_domain(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
    }

    '''新版与旧版解析位置确定'''
    className = r'<iframe\s+class="n_downlink"\s+name="\d+"\s+src="([^"]+)"\s+frameborder="0"\s+scrolling="no"></iframe>'
    mathNum = 0
    if type == 'old':
        className = r'<iframe\s+class="ifr2"\s+name="\d+"\s+src="([^"]+)"\s+frameborder="0"\s+scrolling="no"></iframe>'
        mathNum = 1

    response = requests.get(url, headers=headers)
    iframe_pattern = re.compile(className)
    matches = iframe_pattern.findall(response.text)
    response2 = requests.get(f"https://{doMain}{matches[mathNum]}", headers=headers)
    sign = extract_link(response2.text, r"'sign'\s*:\s*'([^']+)'")
    url2 = extract_link(response2.text, r"url\s*:\s*'([^']+)'")
    data = {
        'action': 'downprocess',
        'signs': '?ctdf',
        'sign': sign,
        'websign': '',
        'websignkey': 'bL27',
        'ves': 1
    }
    headers = {
        "Referer": matches[mathNum],
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
    }
    response3 = requests.post(f"https://{doMain}{url2}", headers=headers, data=data)
    data = json.loads(response3.text)
    full_url = data['dom'] + "/file/" + data['url']
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "cookie": "down_ip=1"
    }
    response4 = requests.get(full_url, headers=headers, allow_redirects=False)
    return response4.headers['Location']
