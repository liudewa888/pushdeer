# 通知
import requests
send_key = {}
def push(type,text,link=None):
  url = f'https://api2.pushdeer.com/message/push?pushkey={send_key["token"]}&text={type}: {text}'
  if link:
    url = f'https://api2.pushdeer.com/message/push?pushkey={send_key["token"]}&text={type}: {text}&desp=[直达链接]({link})'
  requests.get(url)