import time
from datetime import datetime

from script.push import push
from bili.index import monitor_bili,monitor_bili_moda,monitor_bili_test,monitor_bili_moda_live
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
      main()
    except Exception as e:
      print("程序异常退出", e)
      # push('程序异常退出','请登录远程查看原因')