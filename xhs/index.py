import requests
import time
import re
from script.push import push_dingding_test
push_text_len = 20
platform_name='(小红书)'
up_list = [    
    {
        'id': '0',
        'name': '罗洄头',
        'mid': '6534ea9b000000000400abdd'
    }
]

live_start_time = None
noLogin = False
log_xhs = {}
Wlog_info = None
headers_xhs={
    'Accept': 'text/html,application/xhtml+xml,application/xml;',
    'Cookie': '',
    'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
}

m_tg_last = {}
def xhs_home(UP):
 if UP['mid'] not in m_tg_last:
  m_tg_last[UP['mid']] = ''

 url = 'https://www.xiaohongshu.com/user/profile/' + UP['mid']
 res = requests.get(url,headers=headers_xhs)
 html_content = res.text
 if not html_content:
  return
 html_content = html_content.split('window.__INITIAL_STATE__')

 match = re.search(r'"displayTitle":"(.*?)"', html_content[1])

 if match:
    text = match.group(1)
    text = text.replace('\n',' ')[0:push_text_len]
    id = text
    link = url
    if(m_tg_last[UP['mid']] == ''):
        m_tg_last[UP['mid']] = id
    elif(m_tg_last[UP['mid']] != id):
        push_dingding_test(UP["name"]+'最新动态' + platform_name,text,link)
        m_tg_last[UP['mid']] = id
            
def xhs_main():
  global Wlog_info
  global up_list
  Wlog_info = log_xhs['Wlog_info']
  for i in range(len(up_list)):
    UP = up_list[i]
    xhs_home(UP)
    time.sleep(6 * 2)