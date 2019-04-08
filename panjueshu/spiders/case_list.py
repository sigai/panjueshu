# -*- coding: utf-8 -*-
import hashlib
from time import time
from urllib.parse import urlencode
import json

from redis import Redis, ConnectionPool
import scrapy
from scrapy import Request
from panjueshu.items import CaseItem

class ListSpider(scrapy.Spider):
    name = 'list'
    allowed_domains = ['panjueshu.com']
    base_url = 'http://api.panjueshu.com/Verdict/GetCaseDetails'
    custom_settings = {
        "RETRY_ENABLED": False,
        "LOG_LEVEL": "INFO",
        "DEFAULT_REQUEST_HEADERS": {
            'Charset': 'UTF-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; ONEPLUS A5000 Build/LMY48Z)',
            'Host': 'api.panjueshu.com',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        "ITEM_PIPELINES": {
            "panjueshu.pipelines.PanjueshuPipeline": 300
        }
    }
    pool = ConnectionPool()
    r = Redis(connection_pool=pool)

    def start_requests(self):
        for i in range(0, 23934152, -1):
            ctime = str(round(time()), encoding="utf-8")
            code = self._sig(ctime)
            parameters = {
                "caseid": i,
                "code": code,
                "time": ctime,
            }
            yield Request(
                url=self.base_url, 
                method="POST", 
                body=urlencode(parameters)
                )
            break

    def parse(self, response):
        res = json.loads(response.body_as_unicode())
        code = res["Result"]
        if "200" == code:
            case = res["Details"]
            yield CaseItem(case=case)

    @staticmethod
    def _sig(t, s='panjueshu.com'):
        st = str(t, encoding="utf-8")
        sig_str = st[2:] + st[0:2] + s
        m = hashlib.md5()
        m.update(bytes(sig_str, encoding="utf-8"))
        return m.hexdigest()