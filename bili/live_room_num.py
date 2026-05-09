import requests
from requests.models import Response
import hashlib
from urllib.parse import quote, urlencode
import time
from datetime import datetime
from script.push import push_dingding_sign_by_up
from utils.utils import load_json, save_json
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
            error_response._content = b'{"error": "Request error"}'
            print('TimeoutSession: Request error ' + str(args[1]))
            return error_response


requests_session = TimeoutSession(default_timeout=(5, 12))

live_config = {}
global_config_file1 = "live_"
global_config_file2 = "_config.json"


def get_viewer():
    """替换成你的真实获取逻辑"""
    import random
    return random.randint(100, 1000)


def calc_stats(counts):
    start_idx = int(len(counts) * 15 / 70)
    end_idx = int(len(counts) * 62 / 70) + 1
    if start_idx >= len(counts):
        start_idx = 0
    if end_idx > len(counts):
        end_idx = len(counts)
    if start_idx >= end_idx:
        # 数据量不足时，使用全部数据
        trimmed = counts
    else:
        trimmed = counts[start_idx:end_idx]
    peak = max(trimmed, default=0)
    avg = round(sum(trimmed) / len(trimmed), 2) if trimmed else 0.0
    return peak, avg

# ---------- 主流程 ----------


def live_room_num_start(UP):
    roomId = UP['roomId']
    if not live_config.get(roomId):
        start_time = datetime.now().strftime("%Y-%m-%d")
        live_config[roomId] = {
            'date': start_time,
            'counts': [],
            'peak': None,
            'average': None
        }
    else:
        cnt = get_viewer()
        live_config[roomId]['counts'].append(cnt)



def live_room_num_end(UP):
    record =  live_config[UP['roomId']]
    peak, avg = calc_stats(record['counts'])
    record['peak'] = peak
    record['average']= avg
    filePath = global_config_file1 + UP['roomId'] + global_config_file2
    hist = load_json(filePath)
    hist.append(record)
    save_json(filePath, hist)
    msg_data = {
          'label': UP["name"],
          'title': '直播间人数统计',
          'content':  f'日峰值: ${peak} 日均值: ${avg}',
    }
    push_dingding_sign_by_up(UP, msg_data)
    # 近5次统计
    # last5 = hist[-5:]
    # peaks = [r["max"] for r in last5]
    # avgs = [r["average"] for r in last5]
    # print(f"📈 近5次峰值均值={sum(peaks)/len(peaks):.2f}，均值均值={sum(avgs)/len(avgs):.2f}")
