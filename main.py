import time
import configparser
from datetime import datetime
from script.push import send_key,push
from bili.index import headers_bili,monitor_bili,monitor_bili_moda,monitor_bili_test,monitor_bili_moda_live
# 读取配置文件
def readConfig():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    send_key['token'] = config['data']['send_key']
    headers_bili['Cookie'] = config['data']['cookie_bili']
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
      print("程序异常退出", e)
      push('程序异常退出','请登录远程查看原因')