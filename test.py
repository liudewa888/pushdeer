import time
import os
import configparser
from datetime import datetime
from script.push import push
from bili.index import monitor_bili,monitor_bili_moda,monitor_bili_test,monitor_bili_moda_live
ii = 0
pid = os.getpid()
m_config = configparser.ConfigParser()
# 写入监控配置项
def w_monitor(mark=-1):
      global pid
      global m_config
      global ii
      restart_count = 0
      m_config.read('./monitor.ini')
      if 'monitor' in m_config:
        restart_count = m_config['monitor']['restart_count']
      if ii == 1:
        restart_count = int(restart_count) + 1
      if ii == 31:
        restart_count = 0
      m_config['monitor']={'pid':pid,'mark':mark,'restart_count':restart_count}
      with open('monitor.ini', 'w') as configfile:  
        m_config.write(configfile)

def main():
    global ii
    while(True):
      # now = datetime.now()
      # print("当前轮次" + str(ii) +': ', now.strftime("%Y-%m-%d %H:%M:%S"))
      # monitor_bili()
      # monitor_bili_moda()
      # monitor_bili_test()
      # monitor_bili_moda_live()
      ii = ii + 1
      w_monitor(ii)
      time.sleep(5 * 1)
      if ii > 5:
        time.sleep(10 * 2)

if __name__ == '__main__':
    print('------ 开始监控 ------')
    main()
      # push('程序异常退出','请登录远程查看原因')