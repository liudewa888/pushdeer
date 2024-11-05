
from time import sleep
from http.cookiejar import LWPCookieJar
import requests
from re import findall
from os import path
from io import BytesIO
from PIL import Image
from qrcode import QRCode
from urllib.parse import unquote
import json

temp_cookie_file = 'bz-cookie.txt'
headers = {
    'authority': 'api.vc.bilibili.com', 'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://message.bilibili.com', 'referer': 'https://message.bilibili.com/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
    'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81',
}

def is_login(session):
    try:
        session.cookies.load(ignore_discard=True)
    except Exception as e:
        print(e)
    login_url = session.get("https://api.bilibili.com/x/web-interface/nav", verify=False, headers=headers).json()
    if login_url['code'] == 0:
        print(f"Cookies值有效, {login_url['data']['uname']}，已登录！")
        return True
    else:
        print('Cookies值已经失效，请重新扫码登录！')
        return False

def scan_code(session2):
    get_login = session2.get('https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header', headers=headers).json()
    qrcode_key = get_login['data']['qrcode_key']
    qr = QRCode()
    qr.add_data(get_login['data']['url'])
    img = qr.make_image()
    img.save('bilibili_qrcode.png')
    print('请扫描以下二维码进行登录：')
    print(get_login['data']['url'])
    token_url = f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}&source=main-fe-header'
    while True:
        qrcode_data = session2.get(token_url, headers=headers).json()
        if qrcode_data['data']['code'] == 0:
            print('扫码成功')
            session2.get(qrcode_data['data']['url'], headers=headers)
            break
        else:
            print(qrcode_data['data']['message'])
        sleep(3)
    session2.cookies.save()

def bz_login():
    login_session = requests.session()
    login_session.cookies = LWPCookieJar(filename=temp_cookie_file)
    status = is_login(login_session)
    if not status:
        scan_code(login_session)
    else:
        cookies_dict = requests.utils.dict_from_cookiejar(login_session.cookies)
        cookies_str = '; '.join([f"{key}={value}" for key, value in cookies_dict.items()])
        cookies_str_decoded=unquote(cookies_str)
        with open('bili_cookie.txt', 'w') as file:
            file.write(cookies_str_decoded)

if __name__ == '__main__':
    if not path.exists(temp_cookie_file):
        with open(temp_cookie_file, 'w', encoding='utf-8') as f:
            f.write("")
    with open(temp_cookie_file, 'r', encoding='utf-8') as f:
        bzcookie = f.read()
    requests.packages.urllib3.disable_warnings()
    bz_login()
