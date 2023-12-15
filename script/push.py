# 通知
import requests
send_key = {}
def push(type,text,link=None,desc=None):
  tokens = send_key["token"].split(',')
  url = 'https://api2.pushdeer.com/message/push'
  desp = ''
  if desc:
    desp = desp +"#### 帖子: " + desc + " \n "
  if link:
    desp = desp + f'#### [直达链接]({link})'
  for i in range(len(tokens)):
    data ={
      'pushkey': tokens[i],
      'text': type + ': ' +text,
      'desp': desp
    }
    requests.post(url,data)