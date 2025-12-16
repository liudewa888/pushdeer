import time
import requests
from requests.models import Response
from config import http_proxy_url

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
            print("TimeoutSession: Request error " + str(args[1]))
            return error_response


requests_session = TimeoutSession(default_timeout=(5, 12))


current_ip = {}




def get_proxy_ip():
    global current_ip
    tt = current_ip.get("expireTimeMillis")
    if tt:
        ts13 = int(time.time() * 1000)
        if ts13 + 30000 < int(tt):
            return current_ip['ip']

    response = requests_session.get(http_proxy_url)
    try:
        res = response.json()
    except requests.exceptions.JSONDecodeError:
        return

    if not res.get("data"):
        return
    list = res.get("data")
    current_ip = list[0]
    return current_ip["ip"]
