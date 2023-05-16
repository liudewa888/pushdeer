import requests
from script.push import push
m_tg = ''
def monitor_bili():
    global m_tg
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid=525121722&timezone_offset=-480&features=itemOpusStyle'
    response = requests.get(url)
    res = response.json()
    id = res['data']['items'][0]['id_str']
    type = res['data']['items'][0]['type'].split('_')[2]
    text = res['data']['items'][0]['modules']['module_dynamic']['desc']
    if text:
        text = text['text'][0:16]
    else:
        text = res['data']['items'][0]['modules']['module_dynamic']['major']
        if text:
            text = text['archive']['title'][0:16]
    if(m_tg == ''):
        m_tg = id
    elif(m_tg != id):
        push('莫大最新动态: ',type+' ' + text)
        m_tg = id

m_tg_top = ''
noLogin = False
def monitor_bili_moda():
    global m_tg_top
    global noLogin
    if noLogin:
        return
    cookie = ''
    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?offset=&host_mid=525121722&timezone_offset=-480&features=itemOpusStyle'
    headers={
        'cookie':cookie
    }
    res = requests.get(url,headers=headers).json()

    list = res['data']['items']
    # print(list[0])
    bool = False
    jump_id = ''
    for i in range(len(list)):
        if(list[i]['modules']['module_tag']['text']=='置顶'):
            basic = list[i]['basic']
            readOnly = basic['is_only_fans']
            if readOnly:
              bool = True
              jump_id = basic['jump_url'].split('/opus/')[1]
            break
    if bool:
        url = f'https://api.bilibili.com/x/v2/reply/main?csrf=fcce6f152bd72daf7b7ca4e9db826f77&mode=3&oid={jump_id}&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=0&type=17'
        res = requests.get(url,headers=headers).json()
        reply = res['data']['top_replies'][0]
        top_id = reply['rpid_str']
        # print(reply['content']['message'])
        if m_tg_top == '':
            m_tg_top = top_id
        elif top_id != m_tg_top:
            top_msg = reply['content']['message'][0:16]
            push('莫大置顶最新动态',top_msg)
            m_tg_top = top_id
    else:
        push('莫大置顶动态失效','请重新登录')    
        noLogin = True