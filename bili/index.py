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
        push('B站莫大动态: ',type+' ' + text)
        m_tg = id
