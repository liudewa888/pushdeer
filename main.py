import sys
import time
import random
import configparser
import logging
from script.push import send_key,push,push_dynamic,push_dingding,ding_key,error_key,push_error,ad
from bili.index import headers_bili,bili_main,log
# 读取配置文件
def readConfig():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    if 'data' in config:
      send_key['token'] = config['data']['send_key']
      headers_bili['Cookie'] = config['data']['cookie_bili']
      ding_key['token'] = config['data']['ding_key']
      error_key['token'] = config['data']['error_key']
      ad['ad_info'] = config['data']['ad_info']
    else:
      Wlog_error('配置文件未找到或格式错误')
      sys.exit(0)
# 写入日志
logging.basicConfig(filename='running.log',format='\n%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
def Wlog_error(text):
 logging.error(text,exc_info=True)

def Wlog_info(text):
 logging.info(text)

log['Wlog_info'] = Wlog_info
def test():
  if(ii==1):
    text = '测试...,test...'
    # push('笨笨动态测试',text)
    # push_dynamic('莫大',4,text)
    # push_dingding('莫大置顶','测试怎么说哈哈哈侃侃保证啥只会哈哈','http://baidu.com')
    # push_error('异常','程序异常退出,请登录远程查看日志')
    Wlog_info(text)
ii = 0
def main():
    global ii
    while(True):
      ii = ii + 1
      Wlog_info("当前轮次: " + str(ii))
      # test()
      bili_main()
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
