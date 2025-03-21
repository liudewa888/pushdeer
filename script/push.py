# 通知
import requests
import json
send_key = {}
ding_key= {}
ding_key_benben= {}
ding_key_test= {}
error_key = {}
ad = {}
DING_URL ='https://oapi.dingtalk.com/robot/send?access_token='
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

def push_error(type,text,link=None,desc=None):
  token = error_key["token"]
  url = 'https://api2.pushdeer.com/message/push'
  desp = ''
  if desc:
    desp = desp +"#### 帖子: " + desc + " \n "
  if link:
    desp = desp + f'#### [直达链接]({link})'
  data ={
    'pushkey': token,
    'text': type + ': ' +text,
    'desp': desp
  }
  requests.post(url,data)

def push_dynamic(name,type,content,link=None,ctime=None):
  url="http://10.0.16.17:8002/dynamic/add"
  # url="http://127.0.0.1:9080/moda/dynamic/add"
  # url="http://liudewa.cc/moda/dynamic/add"
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

def push_dingding(type,content,link=None,desc=None):
  headers = {'Content-Type':'application/json'}
  if content and isinstance(content,str):
    text1 = content[0:20]

  text = f'#### { type} \n\n {content}'
  if link:
    text = f'#### { type} \n\n {content} \n\n [直达链接]({link})'
  
  if desc:
     text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {desc}'

  if ad['ad_info']:
   if desc:
      text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {desc} \n\n {ad["ad_info"]}'
   else:
      text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {ad["ad_info"]}'

  data= {
        "msgtype":"markdown",
        "markdown":{
            "title": '通知 '  + type + ' '  + text1,
            "text": text
        }
    }
  
  tokens = ding_key["token"].split(',')
  for i in range(len(tokens)):
    url="https://oapi.dingtalk.com/robot/send?access_token=" + tokens[i]
    requests.post(url,json.dumps(data),headers=headers)

def push_dingding_single(UP,type,content,link=None,desc=None):
  if UP['mid'] != '11473291':
    return
  type = UP['name'] + type
  headers = {'Content-Type':'application/json'}
  if content and isinstance(content,str):
    text1 = content[0:20]

  text = f'#### { type} \n\n {content}'
  if link:
    text = f'#### { type} \n\n {content} \n\n [直达链接]({link})'
  
  if desc:
     text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {desc}'

  if ad['ad_info']:
   if desc:
      text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {desc} \n\n {ad["ad_info"]}'
   else:
      text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {ad["ad_info"]}'

  data= {
        "msgtype":"markdown",
        "markdown":{
            "title": '通知 '  + type + ' '  + text1,
            "text": text
        }
    }
  
  tokens = ding_key_benben["token"].split(',')
  for i in range(len(tokens)):
    url="https://oapi.dingtalk.com/robot/send?access_token=" + tokens[i]
    requests.post(url,json.dumps(data),headers=headers)

def push_dingding_test(type,content,link=None,desc=None):
  global DING_URL
  headers = {'Content-Type':'application/json'}
  if content and isinstance(content,str):
    text1 = content[0:20]

  text = f'#### { type} \n\n {content}'
  if link:
    text = f'#### { type} \n\n {content} \n\n [直达链接]({link})'
  
  if desc:
     text = f'#### { type} \n\n {content} \n\n [直达链接]({link}) \n\n {desc}'
  
  data= {
        "msgtype":"markdown",
        "markdown":{
            "title": '通知 '  + type + ' '  + text1,
            "text": text
        }
    }
  
  tokens = ding_key_test["token"].split(',')
  for i in range(len(tokens)):
    url= DING_URL  + tokens[i]
    requests.post(url,json.dumps(data),headers=headers)
