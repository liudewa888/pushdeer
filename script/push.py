# 通知
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json

from config import ding_key_list

send_key = {}
ding_key = {}
ding_key_benben = {}
ding_key_test = {}
ding_key_debug = {}
error_key = {}
ad = {}
# 设置超时时间


class TimeoutSession(requests.Session):
    def __init__(self, default_timeout=(3, 10)):
        super().__init__()
        self.default_timeout = default_timeout

    def request(self, *args, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.default_timeout
        return super().request(*args, **kwargs)


requests_session = TimeoutSession(default_timeout=(5, 12))

ding_key_dicts = {
    'ding_key_debug': ding_key_debug,
}
push_text_len = 120
global_headers = {'Content-Type': 'application/json'}
DING_URL = 'https://oapi.dingtalk.com/robot/send?access_token='


def push(type, text, link=None, desc=None):
    tokens = send_key["token"].split(',')
    url = 'https://api2.pushdeer.com/message/push'
    desp = ''
    if desc:
        desp = desp + "#### 帖子: " + desc + " \n "
    if link:
        desp = desp + f'#### [直达链接]({link})'
    for i in range(len(tokens)):
        if type[:2] == "笨总" and 'HBoNnR03Rtoko' in tokens[i]:
            continue
        data = {
            'pushkey': tokens[i],
            'text': type + ': ' + text,
            'desp': desp
        }
        requests_session.post(url, data)


def push_error(type, text, link=None, desc=None):
    token = error_key["token"]
    url = 'https://api2.pushdeer.com/message/push'
    desp = ''
    if desc:
        desp = desp + "#### 帖子: " + desc + " \n "
    if link:
        desp = desp + f'#### [直达链接]({link})'
    data = {
        'pushkey': token,
        'text': type + ': ' + text,
        'desp': desp
    }
    requests_session.post(url, data)


def push_dynamic(name, type, content, link=None, ctime=None):
    print('stop: ' + name)
    # url="http://10.0.16.17:8002/dynamic/add"
    # # url="http://127.0.0.1:9080/moda/dynamic/add"
    # # url="http://liudewa.cc/moda/dynamic/add"
    # if content and isinstance(content,str):
    #   content = content[0:20]
    # data = {
    #   'name': name,
    #   'type': type,
    #   'content': content,
    #   'link': link,
    #   'ctime': ctime
    # }
    # requests_session.post(url,data)


def push_dingding(type, content, link=None, desc=None):

    global DING_URL
    global push_text_len
    global global_headers
    title = ''
    if content and isinstance(content, str):
        title = content[0:push_text_len]
    text = f'#### { type} \n\n {content}'
    if link:
        text = f'{text} \n\n [直达链接]({link})'

    if desc:
        text = f'{text} \n\n {desc}'

    if ad['ad_info']:
        text = f'{text} \n\n {ad["ad_info"]}'

    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": '通知 ' + type + ' ' + title,
            "text": text
        }
    }

    tokens = ding_key["token"].split(',')
    for i in range(len(tokens)):
        url = DING_URL + tokens[i]
        requests_session.post(url, json.dumps(data), headers=global_headers)


def push_dingding_single(UP, type, content, link=None, desc=None):
    global DING_URL
    global push_text_len
    global global_headers
    if UP['mid'] not in ('11473291', '665bede70000000007007529'):
        return
    type = UP['name'] + ' ' + type
    title = ''
    if content and isinstance(content, str):
        title = content[0:push_text_len]
    text = f'#### { type} \n\n {content}'
    if link:
        text = f'{text} \n\n [直达链接]({link})'

    if desc:
        text = f'{text} \n\n {desc}'

    if ad['ad_info']:
        text = f'{text} \n\n {ad["ad_info"]}'
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": '通知 ' + type + ' ' + title,
            "text": text
        }
    }

    tokens = ding_key_benben["token"].split(',')
    for i in range(len(tokens)):
        url = DING_URL + tokens[i]
        requests_session.post(url, json.dumps(data), headers=global_headers)


def push_dingding_test(type, content, link=None, desc=None):
    global DING_URL
    global push_text_len
    global global_headers
    title = ''
    if content and isinstance(content, str):
        title = content[0:push_text_len]
    text = f'#### { type} \n\n {content}'
    if link:
        text = f'{text} \n\n [直达链接]({link})'

    if desc:
        text = f'{text} \n\n {desc}'

    if ad['ad_info']:
        text = f'{text} \n\n {ad["ad_info"]}'
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": '通知 ' + type + ' ' + title,
            "text": text
        }
    }

    tokens = ding_key_test["token"].split(',')
    for i in range(len(tokens)):
        url = DING_URL + tokens[i]
        requests_session.post(url, json.dumps(data), headers=global_headers)


def get_dingding_sign(secret):
    # 获取当前时间戳（毫秒）
    timestamp = str(round(time.time() * 1000))
    # 计算签名
    secret_enc = secret.encode('utf-8')
    string_to_sign = f"{timestamp}\n{secret}"
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    return f'&timestamp={timestamp}&sign={sign}'


def push_dingding_by_sign(msg_data, token_keys=[]):
    global DING_URL
    global push_text_len
    global global_headers
    tokens = []
    for i in range(len(token_keys)):
        tokens = tokens + ding_key_dicts[token_keys[i]]["token"].split(',')

    for i in range(len(tokens)):
        item = tokens[i].split('&&')
        token = item[0]
        secret = item[1]
        url = DING_URL + token + get_dingding_sign(secret)

        title_temp = msg_data['label'] + ' ' + msg_data['title']

        title = f'{title_temp} {msg_data["content"][0:push_text_len]}'

        text = f'#### { title_temp } \n\n {msg_data["content"]}'
        if 'link' in msg_data:
            text = f'{text} \n\n [直达链接]({msg_data["link"]})'
        if 'img' in msg_data:
            text = f'{text} \n\n ![图片]({msg_data["img"]})'
        if ad['ad_info']:
            text = f'{text} \n\n {ad["ad_info"]}'

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }
        requests_session.post(url, json.dumps(data), headers=global_headers)


def push_dingding_sign_by_up(UP, msg_data, token_keys=[]):
    global ding_key_list
    global DING_URL
    global push_text_len
    global global_headers
    tokens = []
    ads = []
    if len(token_keys) < 1:
        token_keys = UP['keys']

    for item in token_keys:
        current = next(
            (item1 for item1 in ding_key_list if item1['mid'] == item), None)
        if current and UP['mid'] in current['ups']:
            tokens = tokens + current['ding_keys']
            ads.extend([current.get('ad', False)] * len(current['ding_keys']))

    for i, tokenTemp in enumerate(tokens):
        item = tokenTemp.split('&&')
        token = item[0]
        secret = item[1]
        url = DING_URL + token + get_dingding_sign(secret)

        title_temp = msg_data['label'] + ' ' + msg_data['title']

        title = f'{title_temp} {msg_data["content"]}'

        title = title[0:push_text_len]
        text = ''
        if bool(title_temp.strip()):
            text = f'##### **{ title_temp.strip() }**'
        if msg_data.get("content"):
            text = f'{text} \n\n {msg_data["content"]}'

        if msg_data.get('link'):
            text = f'{text} \n\n [直达链接]({msg_data["link"]})'
        if msg_data.get('img'):
            text = f'{text} \n\n ![图片]({msg_data["img"]})'
        if ad.get('ad_info'):
            if len(ads) > i and ads[i]:
                text = f'{text} \n\n {ad["ad_info"]}'

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }
        requests_session.post(url, json.dumps(data), headers=global_headers)
