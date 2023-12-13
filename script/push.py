# 通知
import requests
send_key = {}
def push(type,text,link=None):
  tokens = send_key["token"].split(',')
  for i in range(len(tokens)):
    url = f'https://api2.pushdeer.com/message/push?pushkey={tokens[i]}&text={type}: {text}'
    if link:
      url = f'https://api2.pushdeer.com/message/push?pushkey={tokens[i]}&text={type}: {text}&desp=[直达链接]({link})'
    requests.get(url)