# 通知
import requests
import json
send_key = {}
ding_key= {}
def push(type,text,link=None,desc=None):
  tokens = send_key["token"].split(',')
  url = 'https://api2.pushdeer.com/message/push'
  desp = ''
  if desc:
    desp = desp +"#### 帖子: " + desc + " \n "
  if link:
    desp = desp + f'#### [直达链接]({link})'
  for i in range(len(tokens)):
    if type[:2] == "笨笨" and 'HBoNnR03Rtoko' in tokens[i]:
      continue
    data ={
      'pushkey': tokens[i],
      'text': type + ': ' +text,
      'desp': desp
    }
    requests.post(url,data)


def push_dynamic(name,type,content,link=None,ctime=None):
  url="http://127.0.0.1/moda/dynamic/add"
  # url="http://127.0.0.1:9080/moda/dynamic/add"
  # url="http://www.yztpsg.cn/moda/dynamic/add"
  if content and isinstance(content,str):
    content = content[0:20]
  data = {
    'name': name,
    'type': type,
    'content': content,
    'link': link,
    'ctime': ctime
  }
  requests.post(url,data)

def push_dingding(type,content,link=None,ctime=None):
  headers = {'Content-Type':'application/json'}
  url="https://oapi.dingtalk.com/robot/send?access_token=" + ding_key['token']
  if content and isinstance(content,str):
    content = content[0:20]
    data= {
        "msgtype":"markdown",
        "markdown":{
            "title": '通知 '  + type + ' '  + content,
            "text": f'#### { type} \n\n {content} \n\n [直达链接]({link})'
        }
    }
  requests.post(url,json.dumps(data),headers=headers)