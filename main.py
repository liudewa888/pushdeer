import sys
import time
import configparser
import logging
from datetime import datetime
from script.push import send_key,push
from bili.index import headers_bili,monitor_bili,monitor_bili_moda,monitor_bili_test,monitor_bili_moda_live
# 读取配置文件
def readConfig():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    if 'data' in config:
      send_key['token'] = config['data']['send_key']
      headers_bili['Cookie'] = config['data']['cookie_bili']
    else:
      print('配置文件未找到或格式错误')
      sys.exit(0)
# 定入日志
logging.basicConfig(filename='error.log',format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR)
def Wlog(text):
 logging.error(text,exc_info=True)

ii = 0
def main():
    global ii
    while(True):
      now = datetime.now()
      print("当前轮次" + str(ii) +': ', now.strftime("%Y-%m-%d %H:%M:%S"))
      monitor_bili()
      monitor_bili_moda()
      monitor_bili_test()
      monitor_bili_moda_live()
      ii = ii + 1
      time.sleep(60 * 3)
if __name__ == '__main__':
    print('------ 开始监控 ------')
    try:
      readConfig()
      main()
    except Exception as e:
      Wlog('')
      print("程序异常退出", e)
      # push('程序异常退出','请登录远程查看原因')