# 通知
import requests
send_key = {}
def push(type,text):
  url = f'https://api2.pushdeer.com/message/push?pushkey={send_key["token"]}&text={type}: {text}'
  requests.get(url)
