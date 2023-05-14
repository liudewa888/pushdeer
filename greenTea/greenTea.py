import time
import requests
from script.push import push
def monitor():
    m_tg = ''
    while True:
      url = 'https://zz6k.cn/bottle-code/marketing/awardLog/pageForDetail'
      data = {"current":1,"pageSize":1000}
      headers = {'Content-Type': 'application/json'}  # 设置请求头
      response = requests.post(url, json=data, headers=headers)
      res = response.json()
      res =res['records'][0]['createTime']
      if(m_tg == ''):
          m_tg = res
      elif(m_tg != res):
          push('绿茶iphone',res)
          m_tg = res
      time.sleep(60 * 5)