import os
import configparser
import time

def main():
    while True:
      readConfig()
      time.sleep(10 * 6 * 60)

pid=None
mark = -1
restart_count = 0
config = configparser.ConfigParser()
# 读取配置文件
def readConfig():
    global pid
    global mark
    global restart_count
    global config
    config.read('./monitor.ini')
    if 'monitor' in config:
      pid = config['monitor']['pid']
      current_mark = config['monitor']['mark']
      restart_count = config['monitor']['restart_count']
      if current_mark != mark and mark != -1:
        mark = current_mark
      else:
        restart(pid)
    else:
      restart(None)
      return

def restart(pid=None):
    global config
    if pid:
      try:  
        os.kill(int(pid),9)
      except Exception as e:
        print(e)
    if int(restart_count)<4: 
      os.system('start pythonw main.py')
    else:
      config['monitor']["restart_count"] = '0'
      with open('monitor.ini', 'w') as configfile:  
        config.write(configfile)
      os._exit(0)

if __name__ == '__main__':
    main()