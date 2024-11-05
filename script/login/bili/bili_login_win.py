from time import sleep
from http.cookiejar import LWPCookieJar
import requests
from re import findall
from tkinter import StringVar, Tk, messagebox
from os import path
from io import BytesIO
from PIL import Image, ImageTk
from qrcode import QRCode
from tkinter.ttk import Button, Label
from threading import Thread
 
 
temp_cookie_file = 'bz-cookie.txt'
headers = {
    'authority': 'api.vc.bilibili.com', 'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://message.bilibili.com', 'referer': 'https://message.bilibili.com/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81',
}
 
 
def is_login(session):
    try:
        session.cookies.load(ignore_discard = True)
    except Exception as e:
        print(e)
    login_url = session.get("https://api.bilibili.com/x/web-interface/nav", verify = False, headers = headers).json()
    if login_url['code'] == 0:
        print(f"Cookies值有效, {login_url['data']['uname']}, 已登录！")
        return True
    else:
        print('Cookies值已经失效，请重新扫码登录！')
        return False
 
 
def scan_code(session2):
    global bili_jct, tk_image
    get_login = session2.get('https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header', headers = headers).json()
    qrcode_key = get_login['data']['qrcode_key']
    qr = QRCode()
    qr.add_data(get_login['data']['url'])
    img = qr.make_image()
    pil_image_change = img.resize((200, 200), resample = Image.BICUBIC, box = None, reducing_gap = None)
    tk_image = ImageTk.PhotoImage(pil_image_change)
    token_url = f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}&source=main-fe-header'
    v1.set('等待扫码')
    label_code.config(image = tk_image)
    while 1:
        qrcode_data = session2.get(token_url, headers = headers).json()
        if qrcode_data['data']['code'] == 0:
            v1.set('扫码成功')
            session2.get(qrcode_data['data']['url'], headers = headers)
            break
        else:
            v1.set(qrcode_data['data']['message'])
        sleep(1)
    session2.cookies.save()
    with open(temp_cookie_file, 'r', encoding = 'utf-8') as f:
        bzcookie = f.read()
    bili_jct = findall(r'bili_jct=(.*?);', bzcookie)[0]
 
 
def bz_login():
    login_session.cookies = LWPCookieJar(filename = temp_cookie_file)
    status = is_login(login_session)
    if not status:
        scan_code(login_session)
    verification()
 
 
def verification():
    url = 'https://api.bilibili.com/x/web-interface/nav'
    resp1 = login_session.get(url = url, headers = headers).json()
    global tk_image
    if resp1['data']['isLogin']:
        face_url = resp1['data']['face']
        image_bytes = requests.get(face_url).content
        data_stream = BytesIO(image_bytes)
        pil_image = Image.open(data_stream)
        pil_image_change = pil_image.resize((200, 200), resample = Image.BICUBIC, box = None, reducing_gap = None)
        tk_image = ImageTk.PhotoImage(pil_image_change)
        status = "cookie有效！登录成功！"
        v1.set(status)
    else:
        thread_it(bz_login)
    label_code.config(image = tk_image)
 
 
 
def thread_it(func, *args):
    thread = Thread(target = func, args = args, daemon = True)
    thread.start()
 
 
def cancel_login():
    msg1 = messagebox.askyesno(title = "提示", message = "注销后cookie将失效，是否注销登录？")
    if msg1:
        url3 = 'https://passport.bilibili.com/login/exit/v2'
        data3 = {'biliCSRF': f'{bili_jct}'}
        login_session.post(url = url3, headers = headers, data = data3).json()
        verification()
 
 
 
 
if __name__ == '__main__':
    root = Tk()
    v1 = StringVar()
    if not path.exists(temp_cookie_file):
        with open(temp_cookie_file, 'w', encoding = 'utf-8') as f:
            f.write("")
    with open(temp_cookie_file, 'r', encoding = 'utf-8') as f:
        bzcookie = f.read()
    try:
        bili_jct = findall(r'bili_jct=(.*?);', bzcookie)[0]
    except Exception as e:
        print(e)
    requests.packages.urllib3.disable_warnings()
    login_session = requests.session()
    root.geometry('300x225')
    root.title("B站cookie获取")
    thread_it(bz_login)
    btn1 = Button(root, width=10, text='注销登录', command=cancel_login)
    btn1.grid(row=3, column=2)
    label_ver2 = Label(root, textvariable = v1)
    label_ver2.grid(row = 9, column = 1, rowspan = 8, columnspan = 1, sticky = 'n')
    white_image = Image.new('RGB', (200, 200), (256, 256, 256))
    tk_image = ImageTk.PhotoImage(white_image)
    label_code = Label(root, image = tk_image)
    label_code.grid(row = 1, column = 1, rowspan = 8, columnspan = 1, sticky = 'n')
    root.mainloop()