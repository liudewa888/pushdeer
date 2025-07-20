import sys
import time
import random
import configparser
import logging
from script.push import send_key,ding_key,error_key,push_error,ad,ding_key_benben,ding_key_test,ding_key_debug
from bili.index import headers_bili,bili_main,log
from xhs.index import xhs_main,log_xhs
# 读取配置文件
def readConfig():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    if 'data' in config:
      send_key['token'] = config['data']['send_key']
      headers_bili['Cookie'] = config['data']['cookie_bili']
      ding_key['token'] = config['data']['ding_key']
      error_key['token'] = config['data']['error_key']
      ding_key_benben['token'] = config['data']['ding_key_benben']
      ding_key_test['token'] = config['data']['ding_key_test']
      ding_key_debug['token'] = config['data']['ding_key_debug']
      ad['ad_info'] = config['data']['ad_info']
    else:
      Wlog_error('配置文件未找到或格式错误')
      sys.exit(0)
# 写入日志
logging.Formatter.converter = time.localtime
logging.basicConfig(filename='running.log',format='\n%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
def Wlog_error(text):
 logging.error(text,exc_info=True)

def Wlog_info(text):
 logging.info(text)

log['Wlog_info'] = Wlog_info
log_xhs['Wlog_info'] = Wlog_info
def test():
  if(ii==1):
    text = '测试...,test...'
    Wlog_info(text)
ii = 0
def main():
    global ii
    while(True):
      ii = ii + 1
      Wlog_info("当前轮次: " + str(ii))
      # test()
      bili_main()
      xhs_main()
      s = random.randint(30,80)
      time.sleep(s * 2)
if __name__ == '__main__':
    Wlog_info('------ 开始监控 ------')
    try:
      readConfig()
      main()
    except Exception as e:
      Wlog_error('')
      print('程序异常退出',e)
      # push_error('异常','程序异常退出,请登录远程查看日志')
