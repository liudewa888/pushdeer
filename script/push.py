# 通知
import requests
TOKEN = ''

def push(type,text):
  url = f'https://api2.pushdeer.com/message/push?pushkey={TOKEN}&text={type}: {text}'
  requests.get(url)
