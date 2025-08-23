import requests
from requests.models import Response
import hashlib
from urllib.parse import quote, urlencode
import time
from datetime import datetime
import copy
from script.push import push, push_dynamic, push_dingding, push_error, push_dingding_single, push_dingding_test, push_dingding_by_sign

# 设置超时时间


class TimeoutSession(requests.Session):
    def __init__(self, default_timeout=(3, 10)):
        super().__init__()
        self.default_timeout = default_timeout

    def request(self, *args, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.default_timeout
        try:
            return super().request(*args, **kwargs)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            error_response = Response()
            error_response.status_code = 400
            error_response._content = b'{"error": "Request timed out"}'
            Wlog_info('错误: Request timed out')
            return error_response


requests_session = TimeoutSession(default_timeout=(5, 12))

push_text_len = 22
up_list = [
    {
        'id': '0',
        'name': '莫大',
        'uname': '莫大',
        'mid': '525121722',
        'roomId': '23229268'
    },
    {
        'id': '1',
        'name': '笨总',
        'uname': '笨总',
        'mid': '11473291',
        'roomId': '27805029'
    }
]


bili_moda_opus_link = 'https://www.bilibili.com/opus/'
live_start_time = None
noLogin = False
log = {}
Wlog_info = None
headers_bili = {
    'Accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
    'Cookie': '',
    'Host': 'api.bilibili.com',
    'Origin': 'https://space.bilibili.com',
    'Referer': 'https://space.bilibili.com/',
    'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
}


def is_login():
    global noLogin
    global headers_bili
    response = requests_session.get(
        "https://api.bilibili.com/x/web-interface/nav", verify=False, headers=headers_bili)
    if response.status_code != 200:
        return False
    login_res = response.json()
    if login_res['code'] == 0:
        Wlog_info(f"bili cookie值有效, {login_res['data']['uname']}，已登录！")
        return True
    else:
        if not noLogin:
            push_error('异常', 'py_A bili cookie失效,请重新登录')
        Wlog_info('bili cookie失效,请重新登录')
        noLogin = True
        return False


def get_w_rid(params):
    m = urlencode(params, quote_via=quote)
    string = m + "ea1db124af3c7062474693fa704f4ff8"
    w_rid = hashlib.md5(string.encode("utf-8")).hexdigest()
    return w_rid


# UP动态
m_tg = {}


def monitor_bili_dynamic(UP):
    global m_tg
    global noLogin
    global headers_bili
    if UP['mid'] not in m_tg:
        m_tg[UP['mid']] = {
            'id': '',
            'ctime': -1,
            'text': ''
        }
    jump_url = ''
    # url = 'http://liudewa.cc/test/monitor_bili_dynamic.json'
    # response = requests_session.get(url)
    url = f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid={UP["mid"]}&platform=web&features=itemOpusStyle,listOnlyfans,opusBigCover,onlyfansVote,forwardListHidden,decorationCard,commentsNewVersion,onlyfansAssetsV2,ugcDelete,onlyfansQaCard'
    response = requests_session.get(url, headers=headers_bili)
    if response.status_code != 200:
        Wlog_info('monitor_bili_dynamic: not 200')
        return
    res = response.json()
    if 'data' not in res:
        Wlog_info('monitor_bili_dynamic: not data' +
                  str(res['code']) + '---' + res['message'])
        return
    list = res['data']['items'][0]
    if 'module_tag' in list['modules']:
        m_module_tag = list['modules']['module_tag']
        if (m_module_tag['text'] == '置顶'):
            list = res['data']['items'][1]
    rid_str = list['basic']['rid_str']
    type = str(list['basic']['comment_type'])
    id = list['id_str']
    jump_url = bili_moda_opus_link + id
    text = list['modules']['module_dynamic']['desc']
    module_author = list['modules']['module_author']
    ctime = module_author['pub_ts']
    textTemp = ''
    if text:
        text = text['text']
    else:
        text = list['modules']['module_dynamic']['major']
        if 'archive' in text:
            text = text['archive']['title']
        elif 'ugc_season' in text:
            text = text['ugc_season']['title']
        elif 'opus' in text:
            opus = text['opus']
            if 'summary' in opus:
                text = opus['summary']['text']
    if text and isinstance(text, str):
        textTemp = text.replace('\n', ' ')
        text = textTemp[0:push_text_len]
    else:
        Wlog_info(UP['name'] + ' monitor_bili_dynamic：not isinstance str '+id)
        return
    if (m_tg[UP['mid']]['id'] == ''):
        m_tg[UP['mid']]['id'] = id
        m_tg[UP['mid']]['ctime'] = ctime
        m_tg[UP['mid']]['text'] = textTemp
    elif m_tg[UP['mid']]['id'] != id:
        if ctime > m_tg[UP['mid']]['ctime']:
            data = {
                'label': UP["uname"],
                'title': '最新动态',
                'content':  text,
                'link': jump_url
            }
            # push_dingding_by_sign(data, ['ding_key_debug'])
            push_dingding(data['label']+ ' ' +
                          data['title'], data['content'], data['link'])
            push_dingding_test(data['label']+ ' ' +
                               data['title'], data['content'], data['link'])
            push_dingding_single(data['label'],
                                 data['title'], data['content'], data['link'])
            m_tg[UP['mid']]['id'] = id
            m_tg[UP['mid']]['ctime'] = ctime
            m_tg[UP['mid']]['text'] = textTemp
        else:
            data = {
                'label': UP["uname"],
                'title': '被删除动态',
                'content':  m_tg[UP['mid']]['text'],
            }
            # push_dingding_by_sign(data, ['ding_key_debug'])
            push_dingding_test(data['label']+ ' ' +
                               data['title'], data['content'])

    if bool(rid_str):
        UP1 = copy.deepcopy(UP)
        UP1['id'] = '最新动态' + UP1['id'] + rid_str
        UP1['name'] = UP1['name'] + '最新动态'
        monitor_bili_top(UP1, rid_str, jump_url, type)
    else:
        Wlog_info(UP1['name'] + 'monitor_bili_dynamic：rid_str is False')


# UP置顶
m_tg_top = {}


def monitor_bili_top(UP, jump_id='', link='', type=''):
    global m_tg_top
    global noLogin
    global headers_bili

    if UP['id'] not in m_tg_top:
        m_tg_top[UP['id']] = ''
    if noLogin:
        return
    if not bool(jump_id):
        url = f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid={UP["mid"]}'
        response = requests_session.get(url, headers=headers_bili)
        if response.status_code != 200:
            Wlog_info('monitor_bili_top: not 200')
            return
        res = response.json()
        if 'data' not in res:
            if res['code'] == -352:
                is_login()
            Wlog_info('monitor_bili_top: not data' +
                      str(res['code']) + '---' + res['message'])
            return
        list = res['data']['items']
        if (len(list) == 0):
            Wlog_info(UP["name"]+'置顶：list长度为0')
            return
        for i in range(len(list)):
            if 'module_tag' in list[i]['modules']:
                m_module_tag = list[i]['modules']['module_tag']
                if (m_module_tag['text'] == '置顶'):
                    id_str = list[i]['id_str']
                    # basic = list[i]['basic']
                    # 默认类型
                    type = '17'
                    jump_id = id_str
                    link = bili_moda_opus_link + jump_id
                    break
    if bool(jump_id):
        # Wlog_info('def monitor_bili_top: ' + jump_id)
        # (置顶 | 最新)动态前100回复
        monitor_bili_top_reply(
            UP, {'link': link, 'oid': jump_id, 'type': type})
        url = f'https://api.bilibili.com/x/v2/reply/main?csrf=fcce6f152bd72daf7b7ca4e9db826f77&mode=3&oid={jump_id}&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=0&type={type}'
        response1 = requests_session.get(url, headers=headers_bili)
        if response1.status_code != 200:
            return
        res = response1.json()
        if 'data' not in res:
            Wlog_info('monitor_bili_top2: not data' +
                      str(res['code']) + '---' + res['message'])
            return
        data = res['data']
        if 'top_replies' not in data:
            return
        if len(data['top_replies']) < 1:
            if m_tg_top[UP["id"]] == '':
                m_tg_top[UP["id"]] = '-1'
            return
        reply = data['top_replies'][0]
        top_id = reply['rpid_str']
        msg = reply['content']['message']
        rcount = reply['rcount']
        rpid = reply['rpid_str']
        ctime = reply['ctime']
        if msg and isinstance(msg, str):
            msg = msg.replace('\n', ' ')[0:push_text_len]
        else:
            # Wlog_info(UP["name"]+'置顶：没包含msg字段 ---117行')
            return
        if m_tg_top[UP["id"]] == '':
            m_tg_top[UP["id"]] = top_id
        elif top_id != m_tg_top[UP["id"]]:
            top_msg = msg
            # push(UP["name"]+'置顶评论',top_msg, link)
            # push_dynamic(UP["name"],2,top_msg,link,ctime)
            push_dingding(UP["name"]+'最新置顶评论', top_msg, link)
            push_dingding_test(UP["name"]+'最新置顶评论', top_msg, link)
            push_dingding_single(UP, '最新置顶评论', top_msg, link)
            m_tg_top[UP["id"]] = top_id
        monitor_bili_reply({'oid': jump_id, 'link': link,
                           'root': rpid, 'rcount': rcount}, UP)
    else:
        if not is_login():
            noLogin = True


# UP置顶回复
start_reply = {}
end_reply = {}


def monitor_bili_reply(options, UP):
    global start_reply
    global end_reply

    if UP['mid'] not in start_reply:
        start_reply[UP['mid']] = {'rpid': -1, 'mid': -1}

    if UP['mid'] not in end_reply:
        end_reply[UP['mid']] = {'rpid': -1, 'mid': -1}

    end_reply_rpid = int(end_reply[UP['mid']]['rpid'])
    start_reply_rpid = int(start_reply[UP['mid']]['rpid'])
    break_flag = False
    pageSize = 20
    pageTotal = options['rcount'] // pageSize + 1
    for pageIndex in range(pageTotal, 0, -1):
        time.sleep(2)
        url = f'https://api.bilibili.com/x/v2/reply/reply?oid={options["oid"]}&type=17&root={options["root"]}&ps={pageSize}&pn={pageIndex}&web_location=444.42'
        res = requests_session.get(url, headers=headers_bili).json()
        if 'data' not in res:
            Wlog_info('monitor_bili_reply: not data' +
                      str(res['code']) + '---' + res['message'])
            return
        data = res['data']
        if not bool(data) or 'replies' not in data:
            # Wlog_info('replies not in data ---283行')
            return
        replies = data['replies']
        root = data['root']
        root_msg = root['content']['message']
        if root_msg and isinstance(root_msg, str):
            root_msg = '评论: ' + root_msg.replace('\n', ' ')[0:10]
        le = len(replies)-1
        for i in range(le, -1, -1):
            current_start_reply_rpid = int(start_reply[UP['mid']]['rpid'])
            reply = replies[i]
            rpid = reply['rpid_str']
            mid = reply['mid']
            msg = reply['content']['message']
            rpid_int = int(rpid)
            if pageIndex == pageTotal and i == le:
                if end_reply_rpid < rpid_int:
                    ctime = reply['ctime']
                    end_reply[UP['mid']] = {
                        'ctime': ctime, 'mid': mid, 'rpid': rpid}
            if rpid_int <= end_reply_rpid or end_reply_rpid == -1:
                break_flag = True
                break
            if str(mid) == UP["mid"] and start_reply_rpid < rpid_int:
                ctime = reply['ctime']
                if current_start_reply_rpid < rpid_int:
                    start_reply[UP['mid']] = {
                        'ctime': ctime, 'mid': mid, 'rpid': rpid}
                text = msg
                if text and isinstance(text, str):
                    text = text.replace('\n', ' ')[0:push_text_len]
                # push(UP["name"]+'最新置顶评论回复',text,options['link'],root_msg+f'(评论数量: {options["rcount"]})')
                # push_dingding(UP["name"]+'最新置顶评论回复', text, options['link'],
                #               root_msg+f'(评论数量: {options["rcount"]})')
                push_dingding_test(
                    UP["name"]+'最新置顶评论回复', text, options['link'], root_msg+f'(评论数量: {options["rcount"]})')
                # push_dingding_single(
                #     UP, '最新置顶评论回复', text, options['link'], root_msg+f'(评论数量: {options["rcount"]})')
        if (break_flag):
            break


# UP(置顶|最新)动态前100回复
m_top_reply = {}


def monitor_bili_top_reply(UP, options):
    global m_top_reply
    target_list = []
    next_page = ""
    if options["oid"] not in m_top_reply:
        m_top_reply[options["oid"]] = int(time.time())
    is_end = False
    for i in range(5):
        time.sleep(4)
        if is_end:
            break
        wts = int(time.time())
        nextPage = '{"offset":\"%s\"}' % next_page
        params = {
            "mode": 2,
            "oid": options["oid"],
            "pagination_str": nextPage,
            "plat": 1,
            "seek_rpid": "",
            "type": options["type"],
            "web_location": 1315875,
            "wts": wts
        }
        w_rid = get_w_rid(params)
        url = f'https://api.bilibili.com/x/v2/reply/wbi/main'
        params['w_rid'] = w_rid
        response = requests_session.get(
            url, params=params, headers=headers_bili)
        if response.status_code != 200:
            Wlog_info('monitor_bili_top_reply: no 200')
            continue
        res = response.json()
        if 'data' not in res:
            Wlog_info('monitor_bili_top_reply: no data' +
                      str(res['code'])+'---' + res['message'])
            Wlog_info(response.url)
            continue
        data = res['data']
        is_end = data['cursor']['is_end']
        pagination_reply = data['cursor']['pagination_reply']
        if 'next_offset' in pagination_reply:
            next_page = pagination_reply['next_offset']
        if 'replies' not in data:
            Wlog_info('monitor_bili_top_reply: ' + 'no replies ')
            Wlog_info(url)
            continue
        replies = data['replies']
        for item in replies:
            parent_comment = ''
            if 'content' in item:
                parent_comment = item['content']['message']
                if parent_comment and isinstance(parent_comment, str):
                    parent_comment = parent_comment.replace('\n', ' ')[
                        0:push_text_len]
            if str(item['mid']) == UP['mid'] and item['ctime'] > m_top_reply[options["oid"]]:
                data = {
                    'ctime': item['ctime'],
                    'up_content': parent_comment,
                    'oid': item['oid_str'],
                    'root': item['root_str'],
                    'rpid': item['rpid_str'],
                    'parent_comment': None
                }
                target_list.append(data)
                continue

            if not 'up_action' in item:
                continue
            if not item['up_action']['reply']:
                continue

            is_up_reply = False
            if 'replies' in item:
                up_replies = item['replies']
                for item1 in up_replies:
                    if UP['mid'] == str(item1['mid']) and item1['ctime'] > m_top_reply[options["oid"]]:
                        if ('content' not in item1):
                            continue
                        text = item1['content']['message']
                        if text and isinstance(text, str):
                            text = text.replace('\n', ' ')[0:push_text_len]
                        data = {
                            'ctime': item1['ctime'],
                            'up_content': text,
                            'oid': item1['oid_str'],
                            'root': item1['root_str'],
                            'rpid': item1['rpid_str'],
                            'parent_comment': '评论: ' + parent_comment
                        }
                        is_up_reply = True
                        target_list.append(data)
            if not is_up_reply and item['ctime'] > m_top_reply[options["oid"]]:
                data = {
                    'ctime': item['ctime'],
                    'up_content': '评论: ' + parent_comment,
                    'oid': item['oid_str'],
                    'root': item['root_str'],
                    'rpid': item['rpid_str'],
                    'parent_comment': None
                }
                target_list.append(data)
    target_list = sorted(target_list, key=lambda x: x['ctime'], reverse=True)
    if len(target_list) < 1:
        return
    Wlog_info('monitor_bili_top_reply: ' + str(target_list[0]['ctime']))
    if m_top_reply[options["oid"]] < target_list[0]['ctime']:
        m_top_reply[options["oid"]] = target_list[0]['ctime']
    for item2 in target_list:
        content = item2['up_content']
        if bool(item2['parent_comment']):
            content = content + ' \n\n ' + item2['parent_comment']
        data = {
            'label': UP["uname"],
            'title': '(置顶|最新)动态前100回复',
            'content':  content,
            'link': options['link']
        }
        # push_dingding_by_sign(data, ['ding_key_debug'])
        push_dingding_test(data['label'] + ' ' + data['title'], data['content'],
                           data['link'])
        time.sleep(3)


# 计算时间差(分钟)

def get_live_time(start_time):
    current_time = datetime.now()
    time_diff = current_time - start_time
    minute = time_diff.seconds // 60 + 1
    return minute


# UP直播
m_live_f = {}
m_live_s = {}
m_live_t = {}


def monitor_bili_live_roomId(UP):
    global m_live_f
    global m_live_s
    global m_live_t
    if UP['mid'] not in m_live_f:
        m_live_f[UP['mid']] = False

    if UP['mid'] not in m_live_s:
        m_live_s[UP['mid']] = False

    if UP['mid'] not in m_live_t:
        m_live_t[UP['mid']] = None

    url = f'https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo?room_id={UP["roomId"]}'
    live_url = f'https://live.bilibili.com/{UP["roomId"]}?broadcast_type=0&is_room_feed=1'
    headers = copy.deepcopy(headers_bili)
    headers['Host'] = "api.live.bilibili.com"
    try:
        response = requests_session.get(url, headers=headers)
    except Exception as e:
        Wlog_info("直播接口服务器异常323行")
        return
    if response.status_code != 200:
        return
    res = response.json()
    if 'data' not in res:
        if not m_live_s[UP['mid']]:
            push_error('异常', UP["name"]+'直播链接rid失效')
            Wlog_info(UP["name"]+'直播链接rid失效')
            m_live_s[UP['mid']] = True
        return
    else:
        if m_live_s[UP['mid']]:
            m_live_s[UP['mid']] = False
    live = res['data']
    if live:
        live_status = live['live_status']
        if (not m_live_f[UP['mid']] and live_status == 1):
            m_live_t[UP['mid']] = datetime.now()
            m_live_f[UP['mid']] = True
            text = '直播开始啦'
            # push(UP["name"]+'直播',text,live_url)
            # push_dynamic(UP["name"],3,text,live_url)
            push_dingding(UP["name"]+'直播', text, live_url)
            push_dingding_test(UP["name"]+'直播', text, live_url)
            push_dingding_single(UP, '直播', text, live_url)
        if (live_status == 0 and m_live_f[UP['mid']]):
            live_minute = get_live_time(m_live_t[UP['mid']])
            m_live_f[UP['mid']] = False
            text = f'直播结束了(时长: {str(live_minute)}分钟)'
            # push(UP["name"]+'直播',text,live_url)
            # push_dynamic(UP["name"],3,text,live_url)
            push_dingding(UP["name"]+'直播', text, live_url)
            push_dingding_test(UP["name"]+'直播', text, live_url)
            push_dingding_single(UP, '直播', text, live_url)


def bili_main():
    global Wlog_info
    global up_list
    Wlog_info = log['Wlog_info']
    for i in range(len(up_list)):
        UP = up_list[i]
        monitor_bili_dynamic(UP)
        time.sleep(1 * 3)
        monitor_bili_top(UP)
        time.sleep(1 * 3)
        monitor_bili_live_roomId(UP)
