import time
from datetime import datetime

from greenTea.greenTea import monitor_greenTea
from bili.index import monitor_bili

def main():
    ii = 0
    while(True):
      monitor_greenTea()
      monitor_bili()
      now = datetime.now()
      print("当前轮次" + str(ii) +': ', now.strftime("%Y-%m-%d %H:%M:%S"))
      ii = ii + 1
      time.sleep(60 * 5)

if __name__ == '__main__':
    print('开始监控: ',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    main()