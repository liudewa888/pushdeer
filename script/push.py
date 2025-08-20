# 通知
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json
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
push_text_len = 24
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
    headers = {'Content-Type': 'application/json'}
    if content and isinstance(content, str):
        text1 = content[0:20]
    else:
        return

    text = f'#### { type} \n\n {content}'
    if link:
        text = f'#### { type} \n\n {content} \n\n [直达链接]({link})'

    if desc:
        text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {desc}'

    if ad['ad_info']:
        if desc:
            text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {desc} \n\n {ad["ad_info"]}'
        else:
            text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {ad["ad_info"]}'

    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": '通知 ' + type + ' ' + text1,
            "text": text
        }
    }

    tokens = ding_key["token"].split(',')
    for i in range(len(tokens)):
        url = "https://oapi.dingtalk.com/robot/send?access_token=" + tokens[i]
        requests_session.post(url, json.dumps(data), headers=headers)


def push_dingding_single(UP, type, content, link=None, desc=None):
    global DING_URL
    if UP['mid'] not in ('11473291', '665bede70000000007007529'):
        return
    type = UP['name'] + type
    headers = {'Content-Type': 'application/json'}
    if content and isinstance(content, str):
        text1 = content[0:20]
    else:
        return

    text = f'#### { type} \n\n {content}'
    if link:
        text = f'#### { type} \n\n {content} \n\n [直达链接]({link})'

    if desc:
        text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {desc}'

    if ad['ad_info']:
        if desc:
            text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {desc} \n\n {ad["ad_info"]}'
        else:
            text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {ad["ad_info"]}'

    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": '通知 ' + type + ' ' + text1,
            "text": text
        }
    }

    tokens = ding_key_benben["token"].split(',')
    for i in range(len(tokens)):
        url = DING_URL + tokens[i]
        requests_session.post(url, json.dumps(data), headers=headers)


def push_dingding_test(type, content, link=None, desc=None):
    global DING_URL
    headers = {'Content-Type': 'application/json'}
    if content and isinstance(content, str):
        text1 = content[0:push_text_len]
    else:
        return

    text = f'#### { type} \n\n {content}'
    if link:
        text = f'#### { type} \n\n {content} \n\n [直达链接]({link})'

    if desc:
        text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {desc}'

    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": '通知 ' + type + ' ' + text1,
            "text": text
        }
    }

    tokens = ding_key_test["token"].split(',')
    for i in range(len(tokens)):
        url = DING_URL + tokens[i]
        requests_session.post(url, json.dumps(data), headers=headers)


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
    tokens = []
    for i in range(len(token_keys)):
        tokens = tokens + ding_key_dicts[token_keys[i]]["token"].split(',')

    for i in range(len(tokens)):
        item = tokens[i].split('&&')
        token = item[0]
        secret = item[1]
        url = DING_URL + token + get_dingding_sign(secret)
        title = msg_data['label'] + ' ' + msg_data['title'] + \
            f' \n\n {msg_data["content"][0:push_text_len]}'
        text = f'#### { title } \n\n {msg_data["content"]}'
        if 'link' in msg_data:
            text = f'{text} \n\n [直达链接]({msg_data["link"]})'
        if 'img' in msg_data:
            text = f'{text} \n\n ![图片]({msg_data["img"]})'
        # if ad['ad_info']:
        #   text = f'{text} \n\n {ad["ad_info"]}'

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }
        requests_session.post(url, json.dumps(data), headers=global_headers)
