import atexit
import time
from datetime import datetime

from script.push import push
from greenTea.index import monitor_greenTea
from bili.index import monitor_bili,monitor_bili_moda
from liqun.index import monitor_liqun
ii = 0
def main():
    global ii
    while(True):
      now = datetime.now()
      print("当前轮次" + str(ii) +': ', now.strftime("%Y-%m-%d %H:%M:%S"))
      # monitor_greenTea()
      # monitor_liqun()
      monitor_bili()
      monitor_bili_moda()
      ii = ii + 1
      time.sleep(60 * 5)
      # time.sleep(10)

def cleanup():
   global ii
   if ii > 10:
      push('监控异常退出','请登录检查')
atexit.register(cleanup)
if __name__ == '__main__':
    print('------ 开始监控 ------')
    main()