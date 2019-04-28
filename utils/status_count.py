import hashlib
from time import time, sleep
from urllib.parse import urlencode
import json
from datetime import datetime

from redis import Redis, ConnectionPool
import requests


def sig(t, s='panjueshu.com'):
    st = str(t)
    sig_str = st[2:] + st[0:2] + s
    m = hashlib.md5()
    m.update(bytes(sig_str, encoding="utf-8"))
    return m.hexdigest()


headers = {
    'Charset': 'UTF-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; ONEPLUS A5000 Build/LMY48Z)',
    'Host': 'api.panjueshu.com',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    }

base_url = "http://api.panjueshu.com/Verdict/GetCaseType"

def status():
    ctime = round(time())
    code = sig(t=ctime)
    parameters = {
        "code": code,
        "time": ctime,
        }
    res = requests.post(base_url, data=parameters, headers= headers)
    data = res.json()
    update = 0
    total = 0
    for each in data["CaseTypeList"]:
        if each["CaseTypeId"] == 0:
            update = each["CaseTypeCount"]
        if each["CaseTypeId"] == -1:
            total = each["CaseTypeCount"]
    return update, total

if __name__ == '__main__':
    while True:
        now = datetime.now().isoformat(timespec="seconds")
        update, total = status()
        print(f"[{now}] today: {update}\ttotal: {total}")
        sleep(60)