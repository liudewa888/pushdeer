import sys
import os
import requests


headers_bili = {
    'Accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
    'Cookie': '',
    'Host': 'api.bilibili.com',
    'Origin': 'https://space.bilibili.com',
    'Referer': 'https://space.bilibili.com/',
    'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
}

file_path = 'bili_cookie.txt'


def readConfig():
    global headers_bili
    global file_path
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            headers_bili['Cookie'] = file.read().strip()
    else:
        print(f"cookie文件不存在")
        sys.exit(0)


def is_login():
    global headers_bili
    response = requests.get(
        "https://api.bilibili.com/x/web-interface/nav", verify=False, headers=headers_bili)
    if response.status_code != 200:
        return False
    login_res = response.json()
    print(login_res)
    if login_res['code'] == 0:
        print(f"bili cookie值有效, {login_res['data']['uname']}，已登录！")
        return True
    else:
        print('bili cookie失效,请重新登录')
        print(headers_bili['Cookie'])
        return False


def main():
    readConfig()
    is_login()


if __name__ == "__main__":
    main()
