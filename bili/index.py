import requests
from script.push import push
noLogin = False
headers_bili={
    'Accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
    'Cookie': '',
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
    if 'data' not in res:
      return
    list = res['data']['items'][0]
    if 'module_tag' in list['modules']:
      m_module_tag = list['modules']['module_tag']
      if(m_module_tag['text']=='置顶'):
          list = res['data']['items'][1]
    id = list['id_str']
    type = list['type'].split('_')[2]
    text = list['modules']['module_dynamic']['desc']
    if text:
        text = text['text']
    else:
        text = list['modules']['module_dynamic']['major']
        if 'archive' in text:
            text = text['archive']['title']
        elif 'ugc_season' in text:
            text = text['ugc_season']['title']
    if text and isinstance(text,str):
      text = text.replace('\n',' ')[0:16]
    else:
      return
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
    if 'data' not in res:
      return
    list = res['data']['items']
    bool = False
    jump_id = ''
    jump_url = ''
    for i in range(len(list)):
        if 'module_tag' in list[i]['modules']:
          m_module_tag = list[i]['modules']['module_tag']
          if(m_module_tag['text']=='置顶'):
            basic = list[i]['basic']
            readOnly = basic['is_only_fans']
            if readOnly:
              bool = True
              jump_url = basic['jump_url']
              jump_id = jump_url.split('/opus/')[1]
            break
    if bool:
        url = f'https://api.bilibili.com/x/v2/reply/main?csrf=fcce6f152bd72daf7b7ca4e9db826f77&mode=3&oid={jump_id}&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=0&type=17'
        res = requests.get(url,headers=headers_bili).json()
        if 'data' not in res:
          return
        data = res['data']
        if 'top_replies' not in data:
          return
        reply = data['top_replies'][0]
        top_id = reply['rpid_str']
        name = reply['member']['uname']
        msg = reply['content']['message']
        if msg and isinstance(msg,str):
            msg = msg.replace('\n',' ')[0:16]
        else:
          return
        print('莫大最新置顶评论 ', name +' ' +msg)
        if m_tg_top == '':
            m_tg_top = top_id
        elif top_id != m_tg_top:
            top_msg = msg
            push('莫大最新置顶评论 '+name,top_msg,'https:'+jump_url)
            m_tg_top = top_id
    else:
        push('bili cookie 失效','请重新登录')    
        noLogin = True

m_tg_test = ''
def monitor_bili_test():
    global m_tg_test
    global noLogin
    global headers_bili
    jump_url = ''
    text = ''
    if noLogin:
        return
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&page=1&features=itemOpusStyle'
    # res = requests.get(url,headers=headers,verify=False).json()
    res = requests.get(url,headers=headers_bili).json()
    if 'data' not in res:
      return
    list = res['data']['items']
    id = list[0]['id_str']
    basic = list[0]['basic']
    if 'jump_url' in basic:
      jump_url = basic['jump_url']
    desc = list[0]['modules']['module_dynamic']['desc']
    name =list[0]['modules']['module_author']['name']
    major = list[0]['modules']['module_dynamic']['major']
    if desc:
        text = desc['text']
    if major:
        if 'archive' in major:
            archive =  major['archive']
            if 'jump_url' in  archive:
               jump_url = archive['jump_url']
            if not text:
              text = archive['title']
        if 'ugc_season' in major and not text:
            text = major['ugc_season']['title']

    if text and isinstance(text,str):
      text = text.replace('\n',' ')[0:16]
    else:
        return
    print('关注最新动态 ',name +' '+ text)
    if(m_tg_test == ''):
        m_tg_test = id
    elif(m_tg_test != id):
        if jump_url:
           push('关注最新动态 '+name, text,'https:'+jump_url)
        else:
           push('关注最新动态 '+name, text)
        m_tg_test = id
m_live_status = False
m_live_flag = False
def monitor_bili_moda_live():
    global m_live_flag
    global m_live_status
    url = 'https://api.bilibili.com/x/space/wbi/acc/info?mid=525121722&token=&platform=web&web_location=1550101&w_rid=045491671169ffe8a131026b019247d0&wts=1688864515'
    res = requests.get(url,headers=headers_bili).json()
    if 'data' not in res:
        if not m_live_status:
            push('直播状态','莫大链接rid失效')
            m_live_status = True
        return
    else:
        if m_live_status:
            m_live_status = False
    live = res['data']['live_room']
    if live:
        live_status = live['liveStatus']
        live_room_status = live['roomStatus']
        live_title = live['title']
        live_url = live['url']
        print('直播动态','莫大',live_status,live_room_status)
        if(not m_live_flag and live_status == 1):
            print('直播动态','莫大开播了')
            push('直播动态','莫大开播了--'+live_title,live_url)
            m_live_flag = True
        if(live_status == 0):
            m_live_flag = False