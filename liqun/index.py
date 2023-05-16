import requests
from script.push import push
m_tg = ['1643880172304150530','1643880342404149249']
m_t=''
def monitor_liqun():
    global m_tg
    global m_t
    url = 'http://liqunchina.com/service/activity/act/phase/win-record/listByRecently?actId=1643866101438451713'
    # data = {"current":1,"pageSize":1000}
    headers = {
        'Authorization':'Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxNjU4MzE0NDE2MTYyMzM2NzcwIiwicGhvbmUiOiIiLCJpc3MiOiJ3ZWl4aW4tcGxhdGZvcm0iLCJleHAiOjE2ODQyMjA5MjN9.rDX7KSzJgfZJsj24_vcVSzwg7Hk-qJpIydRqD205zsI',
        'Host':'liqunchina.com'
    }
    response = requests.get(url, headers=headers)
    res = response.json()
    one =''
    try:
      one =  res['data'][0]
    except Exception:
       push('利群cookie失效','请重新登录')
       exit()
    id = one['goodsId']
    name = one['goodsName']
    time = one['winTime']
    if(id not in m_tg and m_t != time):
      m_t = time
      print('利群: ',name + ' '+time)
      push('利群',name + ' '+time)
    else:
       print('利群: ',one['goodsName'] + ' '+one['nickname']+ ' ' +  one['winTime'].split(' ')[1])


