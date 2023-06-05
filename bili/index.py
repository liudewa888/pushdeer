import requests
from script.push import push
noLogin = False
cookie_bili =''
headers_bili={
    'Accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
    'Cookie': cookie_bili,
    'Host': 'api.bilibili.com',
    'Origin': 'https://space.bilibili.com',
    'Referer': 'https://space.bilibili.com/525121722/dynamic',
    'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
}
m_tg = ''
def monitor_bili():
    global m_tg
    global noLogin
    global headers_bili
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid=525121722&timezone_offset=-480&features=itemOpusStyle'
    res = requests.get(url,headers=headers_bili).json()
    # print(res)
    list = res['data']['items'][0]
    if 'module_tag' in list['modules']:
      m_module_tag = list['modules']['module_tag']
      if(m_module_tag['text']=='置顶'):
          list = res['data']['items'][1]
    id = list['id_str']
    type = list['type'].split('_')[2]
    text = list['modules']['module_dynamic']['desc']
    if text:
        text = text['text'][0:16]
    else:
        text = list['modules']['module_dynamic']['major']
        if text:
            text = text['archive']['title'][0:16]
    if text:
      text = text.replace('\n','')
      print('莫大最新动态',text)
    if(m_tg == ''):
        m_tg = id
    elif(m_tg != id):
        push('莫大最新动态',text)
        m_tg = id

m_tg_top = ''

def monitor_bili_moda():
    global m_tg_top
    global noLogin
    global headers_bili
    if noLogin:
        return
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid=525121722&timezone_offset=-480&features=itemOpusStyle'
    res = requests.get(url,headers=headers_bili).json()
    list = res['data']['items']
    bool = False
    jump_id = ''
    for i in range(len(list)):
        if 'module_tag' in list[i]['modules']:
          m_module_tag = list[i]['modules']['module_tag']
          if(m_module_tag['text']=='置顶'):
            basic = list[i]['basic']
            readOnly = basic['is_only_fans']
            if readOnly:
              bool = True
              jump_id = basic['jump_url'].split('/opus/')[1]
            break
    if bool:
        url = f'https://api.bilibili.com/x/v2/reply/main?csrf=fcce6f152bd72daf7b7ca4e9db826f77&mode=3&oid={jump_id}&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=0&type=17'
        res = requests.get(url,headers=headers_bili).json()
        reply = res['data']['top_replies'][0]
        top_id = reply['rpid_str']
        name = reply['member']['uname']
        print('莫大最新置顶评论 ', name +' ' +reply['content']['message'])
        if m_tg_top == '':
            m_tg_top = top_id
        elif top_id != m_tg_top:
            top_msg = reply['content']['message'][0:16]
            push('莫大最新置顶评论 '+name,top_msg)
            m_tg_top = top_id
    else:
        push('bili cookie 失效','请重新登录')    
        noLogin = True

m_tg_test = ''
def monitor_bili_test():
    global m_tg_test
    global noLogin
    global headers_bili
    if noLogin:
        return
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&page=1&features=itemOpusStyle'
    # res = requests.get(url,headers=headers,verify=False).json()
    res = requests.get(url,headers=headers_bili).json()
    list = res['data']['items']
    id = list[0]['id_str']
    type = list[0]['type'].split('_')[2]
    text = list[0]['modules']['module_dynamic']['desc']
    name =list[0]['modules']['module_author']['name']
    if text:
        text = text['text'][0:16]
    else:
        text = list[0]['modules']['module_dynamic']['major']
        if text:
            text = text['archive']['title'][0:16]
    print('关注最新动态 ',name +' '+ text)
    if(m_tg_test == ''):
        m_tg_test = id
    elif(m_tg_test != id):
        push('关注最新动态 '+name, text)
        m_tg_test = id
m_live_flag = False
def monitor_bili_moda_live():
    global m_live_flag
    url = 'https://api.bilibili.com/x/space/wbi/acc/info?mid=525121722&token=&platform=web&web_location=1550101&w_rid=7c4a021e017471099db24a5f5e916d8f&wts=1685791381'
    res = requests.get(url,headers=headers_bili).json()
    live = res['data']['live_room']
    if live:
        live_status = live['liveStatus']
        live_room_status = live['roomStatus']
        print('直播动态','莫大',live_status,live_room_status)
        if(not m_live_flag and live_status == 1):
            print('直播动态','莫大开播了')
            push('直播动态','莫大开播了')
            m_live_flag = True
        if(live_status == 0):
            m_live_flag = False