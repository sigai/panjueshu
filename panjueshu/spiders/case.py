# -*- coding: utf-8 -*-
import hashlib
from time import time, sleep
from urllib.parse import urlencode
import json

from redis import Redis, ConnectionPool
import scrapy
from scrapy import Request
from panjueshu.items import CaseItem

class ListSpider(scrapy.Spider):
    name = 'case'
    allowed_domains = ['api.panjueshu.com']
    base_url = 'http://api.panjueshu.com/Verdict/GetCaseDetails'
    custom_settings = {
        "RETRY_ENABLED": False,
        "LOG_LEVEL": "INFO",
        "DOWNLOAD_FAIL_ON_DATALOSS": False,
        "DEFAULT_REQUEST_HEADERS": {
            'Charset': 'UTF-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; ONEPLUS A5000 Build/LMY48Z)',
            'Host': 'api.panjueshu.com',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        "ITEM_PIPELINES": {
            "panjueshu.pipelines.PanjueshuPipeline": 300
        },
        "DOWNLOADER_MIDDLEWARES": {
            "panjueshu.middlewares.PanjueshuDownloaderMiddleware": 543
        }
    }
    pool = ConnectionPool()
    r = Redis(connection_pool=pool)

    def start_requests(self):
        while True:
            for i in range(24844499, 25000000):
                if self.r.sismember("panjueshu:crawled", str(i)):
                    self.logger.info(i)
                    continue
                ctime = round(time())
                code = self._sig(t=ctime)
                parameters = {
                    "caseid": str(i),
                    "code": code,
                    "time": ctime,
                }
                yield Request(
                    url=self.base_url, 
                    method="POST", 
                    body=urlencode(parameters)
                    )

    def parse(self, response):
        try:
            res = json.loads(response.body_as_unicode())
        except Exception:
            Ellipsis
        else:
            code = res["Result"]
            if "200" == code:
                case = res["Details"]
                yield CaseItem(case=case)

    @staticmethod
    def _sig(t, s='panjueshu.com'):
        st = str(t)
        sig_str = st[2:] + st[0:2] + s
        m = hashlib.md5()
        m.update(bytes(sig_str, encoding="utf-8"))
        return m.hexdigest()